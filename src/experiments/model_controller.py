from __future__ import annotations

import os
import threading
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterator, List, Optional, Tuple

from .config import ModelConfig


@dataclass
class ModelControllerStats:
    request_count: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_latency_seconds: float = 0.0
    total_queue_wait_seconds: float = 0.0
    total_request_latency_seconds: float = 0.0
    error_count: int = 0
    max_concurrent_requests: int = 0


class ModelController:
    """Select one provider and provide bounded, concurrency-safe generation."""

    def __init__(
        self,
        config: ModelConfig,
        *,
        seed: int = 0,
        provider: Optional[Any] = None,
        require_credentials: bool = True,
        model_workers: int = 1,
    ):
        if model_workers < 1:
            raise ValueError("model_workers must be at least 1")
        self.config = config
        self.seed = seed
        self.stats = ModelControllerStats()
        self._stats_lock = threading.RLock()
        self._provider_lock = threading.Lock()
        self._langchain_lock = threading.Lock()
        self._task_local = threading.local()
        self._task_stats: Dict[str, ModelControllerStats] = {}
        self._task_in_flight: Dict[str, int] = {}
        self._in_flight = 0
        self._pending_requests = 0
        self._requests_started = False
        self._model_workers = model_workers
        self._request_gate = threading.BoundedSemaphore(model_workers)
        self._provider = provider
        self._langchain_model = None
        self._api_key = None
        if provider is None:
            self._api_key = os.environ.get(config.api_key_env)
            if require_credentials and not self._api_key:
                raise RuntimeError(
                    f"{config.api_key_env} must be set for model backend {config.backend!r}"
                )
            # Construct before worker threads start. The property remains locked as
            # protection for injected/lazily restored controller instances.
            self._provider = self._build_provider()

    @property
    def backend(self) -> str:
        return self.config.backend

    @property
    def model_id(self) -> str:
        return self.config.model_id

    @property
    def model_workers(self) -> int:
        return self._model_workers

    @property
    def provider(self):
        if self._provider is not None:
            return self._provider
        with self._provider_lock:
            if self._provider is None:
                self._provider = self._build_provider()
        return self._provider

    def prepare(self, *, for_langchain: bool = False) -> None:
        """Eagerly initialize shared clients before an executor is launched."""
        _ = self.provider
        if for_langchain:
            self.as_langchain_chat_model()

    def configure_model_workers(self, model_workers: int) -> None:
        """Change the request bound before work starts."""
        if model_workers < 1:
            raise ValueError("model_workers must be at least 1")
        with self._stats_lock:
            if self._requests_started:
                raise RuntimeError(
                    "cannot change model_workers after model requests have started"
                )
            self._model_workers = model_workers
            self._request_gate = threading.BoundedSemaphore(model_workers)

    @contextmanager
    def task_scope(self, task_key: Any) -> Iterator["ModelController"]:
        """Attribute calls in this context to a stable task key.

        The same key may be reused from different worker threads and across
        generation/reflection barriers; all calls accumulate in one task record.
        """
        key = str(task_key)
        if not key:
            raise ValueError("task_key must not be empty")
        marker = object()
        previous = getattr(self._task_local, "task_key", marker)
        self._task_local.task_key = key
        with self._stats_lock:
            self._task_stats.setdefault(key, ModelControllerStats())
        try:
            yield self
        finally:
            if previous is marker:
                del self._task_local.task_key
            else:
                self._task_local.task_key = previous

    def task_stats(self, task_key: Any) -> Dict[str, Any]:
        key = str(task_key)
        with self._stats_lock:
            return asdict(self._task_stats.get(key, ModelControllerStats()))

    def snapshot_task_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._stats_lock:
            return {key: asdict(value) for key, value in self._task_stats.items()}

    def restore_task_stats(self, stats_by_task: Dict[str, Dict[str, Any]]) -> None:
        with self._stats_lock:
            if self._pending_requests:
                raise RuntimeError("cannot restore task stats while requests are pending")
            self._task_stats = {
                str(key): self._stats_from_dict(value)
                for key, value in (stats_by_task or {}).items()
            }
            self._task_in_flight.clear()

    def clear_task_stats(self, task_key: Optional[Any] = None) -> None:
        with self._stats_lock:
            if self._pending_requests:
                raise RuntimeError("cannot clear task stats while requests are pending")
            if task_key is None:
                self._task_stats.clear()
                self._task_in_flight.clear()
            else:
                key = str(task_key)
                self._task_stats.pop(key, None)
                self._task_in_flight.pop(key, None)

    def _build_provider(self):
        if self.config.backend == "openai":
            from models.OpenAI import OpenAIModel

            return OpenAIModel(
                api_key=self._api_key,
                model_id=self.config.model_id,
                base_url=self.config.base_url,
                timeout=self.config.request_timeout_seconds,
            )
        if self.config.backend == "vllm":
            from models.Vllm import VLLMModel

            return VLLMModel(
                api_key=self._api_key,
                model_id=self.config.model_id,
                base_url=self.config.base_url,
                timeout=self.config.request_timeout_seconds,
            )
        raise ValueError(f"unsupported model backend: {self.config.backend}")

    def _common_generate_kwargs(self, overrides: Dict[str, Any]) -> Dict[str, Any]:
        kwargs = {
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "seed": self.seed,
        }
        kwargs.update({key: value for key, value in overrides.items() if value is not None})
        if self.config.backend == "vllm":
            kwargs.setdefault("min_p", self.config.min_p)
            kwargs.setdefault("top_k", self.config.top_k)
            kwargs.setdefault("repetition_penalty", self.config.repetition_penalty)
            kwargs.setdefault("enable_thinking", self.config.enable_thinking)
        return kwargs

    @staticmethod
    def _normalized_usage(usage: Any) -> Tuple[int, int]:
        if usage is None:
            return 0, 0
        if isinstance(usage, dict):
            prompt_tokens = usage.get("prompt_tokens", usage.get("input_tokens", 0))
            completion_tokens = usage.get("completion_tokens", usage.get("output_tokens", 0))
        else:
            prompt_tokens = getattr(
                usage, "prompt_tokens", getattr(usage, "input_tokens", 0)
            )
            completion_tokens = getattr(
                usage, "completion_tokens", getattr(usage, "output_tokens", 0)
            )
        return int(prompt_tokens or 0), int(completion_tokens or 0)

    @staticmethod
    def _record_request(
        stats: ModelControllerStats,
        *,
        prompt_tokens: int,
        completion_tokens: int,
        queue_wait_seconds: float,
        request_latency_seconds: float,
        failed: bool,
        concurrent_requests: int,
    ) -> None:
        stats.request_count += 1
        stats.prompt_tokens += prompt_tokens
        stats.completion_tokens += completion_tokens
        stats.total_queue_wait_seconds += queue_wait_seconds
        stats.total_request_latency_seconds += request_latency_seconds
        stats.total_latency_seconds += queue_wait_seconds + request_latency_seconds
        stats.error_count += int(failed)
        stats.max_concurrent_requests = max(
            stats.max_concurrent_requests, concurrent_requests
        )

    def _run_request(self, operation):
        task_key = getattr(self._task_local, "task_key", None)
        with self._stats_lock:
            self._requests_started = True
            self._pending_requests += 1
            request_gate = self._request_gate
        queued_at = time.monotonic()
        try:
            request_gate.acquire()
        except BaseException:
            with self._stats_lock:
                self._pending_requests -= 1
            raise
        request_started = time.monotonic()
        queue_wait = request_started - queued_at
        with self._stats_lock:
            self._in_flight += 1
            global_concurrency = self._in_flight
            task_concurrency = 0
            if task_key is not None:
                task_concurrency = self._task_in_flight.get(task_key, 0) + 1
                self._task_in_flight[task_key] = task_concurrency

        failed = False
        usage = None
        try:
            result, usage = operation()
            return result
        except BaseException:
            failed = True
            raise
        finally:
            request_latency = time.monotonic() - request_started
            prompt_tokens, completion_tokens = self._normalized_usage(usage)
            with self._stats_lock:
                self._record_request(
                    self.stats,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    queue_wait_seconds=queue_wait,
                    request_latency_seconds=request_latency,
                    failed=failed,
                    concurrent_requests=global_concurrency,
                )
                if task_key is not None:
                    task_stats = self._task_stats.setdefault(
                        task_key, ModelControllerStats()
                    )
                    self._record_request(
                        task_stats,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        queue_wait_seconds=queue_wait,
                        request_latency_seconds=request_latency,
                        failed=failed,
                        concurrent_requests=task_concurrency,
                    )
                    remaining = self._task_in_flight.get(task_key, 1) - 1
                    if remaining:
                        self._task_in_flight[task_key] = remaining
                    else:
                        self._task_in_flight.pop(task_key, None)
                self._in_flight -= 1
                self._pending_requests -= 1
            request_gate.release()

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        provider = self.provider
        generate_kwargs = self._common_generate_kwargs(kwargs)

        def operation():
            response = provider.generate(messages, **generate_kwargs)
            return response, getattr(provider, "last_usage", None)

        return self._run_request(operation)

    def validate_connection(self) -> None:
        try:
            self.provider.client.models.list()
        except Exception as exc:
            raise RuntimeError(
                f"unable to reach {self.config.backend} model endpoint for {self.model_id}: {exc}"
            ) from exc

    def as_langchain_chat_model(self):
        if self._langchain_model is not None:
            return self._langchain_model
        with self._langchain_lock:
            if self._langchain_model is not None:
                return self._langchain_model
            try:
                from langchain_openai import ChatOpenAI
            except ImportError as exc:
                raise RuntimeError(
                    "langchain-openai is required for the LangChain workflow"
                ) from exc

            kwargs = {
                "model": self.config.model_id,
                "api_key": self._api_key,
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "seed": self.seed,
                "timeout": self.config.request_timeout_seconds,
                "max_retries": 0,
            }
            if self.config.backend == "openai":
                from models.OpenAI import requires_max_completion_tokens

                token_parameter = (
                    "max_completion_tokens"
                    if requires_max_completion_tokens(self.config.model_id)
                    else "max_tokens"
                )
            else:
                token_parameter = "max_tokens"
            kwargs[token_parameter] = self.config.max_tokens
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url
            if self.config.backend == "vllm":
                kwargs["extra_body"] = {
                    "min_p": self.config.min_p,
                    "top_k": self.config.top_k,
                    "repetition_penalty": self.config.repetition_penalty,
                    "chat_template_kwargs": {
                        "enable_thinking": self.config.enable_thinking
                    },
                }
            self._langchain_model = ChatOpenAI(**kwargs)
            return self._langchain_model

    def invoke_langchain(self, messages, tools):
        chat_model = self.as_langchain_chat_model()
        bound_model = chat_model.bind_tools(tools)

        def operation():
            response = bound_model.invoke(messages)
            return response, getattr(response, "usage_metadata", None)

        return self._run_request(operation)

    def snapshot_stats(self) -> Dict[str, Any]:
        with self._stats_lock:
            return asdict(self.stats)

    @staticmethod
    def _stats_from_dict(stats: Optional[Dict[str, Any]]) -> ModelControllerStats:
        stats = stats or {}
        defaults = ModelControllerStats()
        values = {
            name: stats.get(name, getattr(defaults, name))
            for name in ModelControllerStats.__dataclass_fields__
        }
        return ModelControllerStats(**values)

    def restore_stats(self, stats: Dict[str, Any]) -> None:
        with self._stats_lock:
            if self._pending_requests:
                raise RuntimeError("cannot restore stats while requests are pending")
            self.stats = self._stats_from_dict(stats)

    def resolved_settings(self) -> Dict[str, Any]:
        settings = asdict(self.config)
        settings["seed"] = self.seed
        settings["model_workers"] = self.model_workers
        settings["api_key_env"] = self.config.api_key_env
        return settings
