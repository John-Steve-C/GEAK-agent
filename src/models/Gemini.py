# Copyright(C) [2025] Advanced Micro Devices, Inc. All rights reserved.

from typing import List
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential
import requests
from models.Base import BaseModel


class GeminiRetryableError(Exception):
    pass


class GeminiModel(BaseModel):
    """Official Google Gemini API client."""

    def __init__(self, 
                 model_id="gemini-2.5-pro-preview-05-06", 
                 api_key=None):
        assert api_key is not None, "no api key is provided."
        self.model_id = model_id
        self.SERVER = "https://generativelanguage.googleapis.com/v1beta"
        self.HEADERS = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        }

    def _model_path(self) -> str:
        if self.model_id.startswith("models/"):
            return self.model_id
        return f"models/{self.model_id}"

    def _message_to_content(self, message: dict) -> dict:
        role = message.get("role", "user")
        if role == "assistant":
            role = "model"
        elif role == "system":
            role = "user"
        elif role not in ("user", "model"):
            role = "user"

        content = message.get("content", "")
        if isinstance(content, str):
            parts = [{"text": content}]
        elif isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append({"text": item})
                elif isinstance(item, dict):
                    if "text" in item or "inline_data" in item or "file_data" in item:
                        parts.append(item)
                    elif item.get("type") == "text":
                        parts.append({"text": item.get("text", "")})
                    else:
                        parts.append({"text": str(item)})
                else:
                    parts.append({"text": str(item)})
        else:
            parts = [{"text": str(content)}]

        return {"role": role, "parts": parts}

    def _build_body(self, messages: List, temperature, presence_penalty,
                    frequency_penalty, max_tokens) -> dict:
        contents = []
        system_parts = []

        for message in messages:
            if message.get("role") == "system":
                system_parts.extend(self._message_to_content(message)["parts"])
            else:
                contents.append(self._message_to_content(message))

        body = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
                "topP": 0.95,
                "presencePenalty": presence_penalty,
                "frequencyPenalty": frequency_penalty,
            },
        }
        if system_parts:
            body["systemInstruction"] = {"parts": system_parts}

        return body
    
    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(GeminiRetryableError),
        reraise=True,
    )
    def _generate_once(self,
                       messages: List,
                       temperature=1.0,
                       presence_penalty=0,
                       frequency_penalty=0,
                       max_tokens=30000) -> str:
        body = self._build_body(
            messages=messages,
            temperature=temperature,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            max_tokens=max_tokens,
        )
        response = requests.post(
            url=f"{self.SERVER}/{self._model_path()}:generateContent",
            json=body,
            headers=self.HEADERS,
            timeout=600,
        )
        if response.status_code == 503:
            raise GeminiRetryableError(f"Gemini API returned status 503: {response.text}")
        if response.status_code != 200:
            raise ValueError(f"Gemini API returned status {response.status_code}: {response.text}")

        result = response.json()
        try:
            candidate = result["candidates"][0]
            finish_reason = candidate.get("finishReason")
            if finish_reason == "MAX_TOKENS":
                usage = result.get("usageMetadata", {})
                raise ValueError(f"Gemini response was truncated by maxOutputTokens: {usage}")
            parts = candidate["content"]["parts"]
            return "".join(part.get("text", "") for part in parts)
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"Unexpected Gemini response format: {result}") from e

    def generate(self, 
                 messages: List, 
                 temperature=1.0, 
                 presence_penalty=0, 
                 frequency_penalty=0, 
                 max_tokens=30000) -> str:
        try:
            return self._generate_once(
                messages=messages,
                temperature=temperature,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
            )
        except Exception:
            return ""
