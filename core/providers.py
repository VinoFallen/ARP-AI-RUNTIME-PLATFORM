# core/providers.py
from abc import ABC, abstractmethod
from typing import AsyncIterator
from .config import settings
import httpx
 
class LLMProvider(ABC):
    @abstractmethod
    async def stream(self, prompt: str, system: str = '') -> AsyncIterator[str]: ...
    @abstractmethod
    async def complete(self, prompt: str, system: str = '') -> str: ...
 
class OllamaProvider(LLMProvider):
    def __init__(self, model='gemma2:2b'):
        self.model = model
        self.base_url = settings.ollama_base_url
 
    async def complete(self, prompt, system='') -> str:
        async with httpx.AsyncClient() as client:
            r = await client.post(f'{self.base_url}/api/generate',
                json={'model': self.model, 'prompt': prompt,
                      'system': system, 'stream': False}, timeout=60)
            return r.json()['response']
 
    async def stream(self, prompt, system='') -> AsyncIterator[str]:
        async with httpx.AsyncClient() as client:
            async with client.stream('POST', f'{self.base_url}/api/generate',
                json={'model': self.model, 'prompt': prompt,
                      'system': system, 'stream': True}, timeout=120) as r:
                async for line in r.aiter_lines():
                    import json
                    chunk = json.loads(line)
                    if not chunk.get('done'):
                        yield chunk.get('response', '')
 
class GeminiProvider(LLMProvider):
    def __init__(self, model='gemini-2.0-flash'):
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(model)
 
    async def complete(self, prompt, system='') -> str:
        response = self.model.generate_content(prompt)
        return response.text
 
    async def stream(self, prompt, system='') -> AsyncIterator[str]:
        for chunk in self.model.generate_content(prompt, stream=True):
            if chunk.text:
                yield chunk.text
 
def get_provider() -> LLMProvider:
    if settings.app_env == 'production' and settings.gemini_api_key:
        return GeminiProvider()
    return OllamaProvider()
