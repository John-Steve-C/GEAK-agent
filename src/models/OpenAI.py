import threading
from typing import List
import openai

from models.Base import BaseModel


def requires_max_completion_tokens(model_id: str) -> bool:
    model_name = str(model_id).lower().rsplit("/", 1)[-1]
    return model_name.startswith(("gpt-5", "o1", "o3", "o4"))


class OpenAIModel(BaseModel):
    def __init__(self, 
                 model_id="GPT4o", 
                 model_api_version='2024-06-01', 
                 api_key=None,
                 base_url=None,
                 timeout=300):
        assert api_key is not None, "no api key is provided."
        self.model_id = model_id
        self.model_api_version = model_api_version

        # assert 'MODEL_API_URL' in os.environ, "MODEL_API_URL environment variable is not set."
        # MODEL_API_URL = os.environ['MODEL_API_URL']

        # url = MODEL_API_URL
        # headers = {
        #     'Ocp-Apim-Subscription-Key': api_key 
        # }
        # model_api_version = '2024-06-01'
        

        # self.client = openai.AzureOpenAI(
        #     api_key='dummy',
        #     api_version=self.model_api_version,
        #     base_url=url,
        #     default_headers=headers
        # )
        # self.client.base_url = '{0}/openai/deployments/{1}'.format(url, self.model_id)
    
        # switch to OpenAI client
        client_kwargs = {"api_key": api_key, "timeout": timeout, "max_retries": 0}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = openai.OpenAI(**client_kwargs)
        self._thread_state = threading.local()
        self.last_usage = {}
    @property
    def last_usage(self):
        return getattr(self._thread_state, "last_usage", {})

    @last_usage.setter
    def last_usage(self, usage):
        self._thread_state.last_usage = usage




    def generate(self, 
                 messages: List, 
                 temperature=0, 
                 presence_penalty=0, 
                 frequency_penalty=0, 
                 max_tokens=5000,
                 top_p=1.0,
                 seed=None,
                 **kwargs) -> str:
        token_limit = (
            {"max_completion_tokens": max_tokens}
            if requires_max_completion_tokens(self.model_id)
            else {"max_tokens": max_tokens, "top_p": top_p}
        )
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=temperature,
            n=1,
            stream=False,
            stop=None,
            # top_p=top_p,
            seed=seed,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logit_bias=None,
            user=None,
            **token_limit,
        )
        if not response or not hasattr(response, 'choices') or len(response.choices) == 0:
            raise ValueError("No response choices returned from the API.")

        usage = getattr(response, "usage", None)
        self.last_usage = {
            "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
            "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
            "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
        }
        return response.choices[0].message.content
      
    # def batch_generate(self,
