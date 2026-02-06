"""
Model Manager Service - LLM Agnostic Router
Handles cross-provider completions and cost tracking.
"""

import logging
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from services.system.api_governance import get_governor
from config.environment_manager import get_settings

logger = logging.getLogger(__name__)

class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"
    OLLAMA = "ollama"
    MOCK = "mock"

@dataclass
class ModelConfig:
    provider: ModelProvider
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 1000

class ModelManager:
    """
    Unified interface for interacting with various LLM providers.
    Supports per-agent model assignment and usage tracking.
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.governor = get_governor()
        logger.info("ModelManager initialized (LLM Agnostic)")

    async def get_completion(self, 
                             prompt: str, 
                             config: ModelConfig, 
                             system_message: str = "You are a helpful investment assistant.") -> str:
        """
        Routes the completion request to the appropriate provider.
        """
        provider_name = config.provider.value.upper()
        
        # 1. Enforce API Governance
        await self.governor.wait_for_slot(provider_name)

        try:
            # 2. Route to specific provider integration
            if config.provider == ModelProvider.OPENAI:
                return await self._call_openai(prompt, config, system_message)
            elif config.provider == ModelProvider.ANTHROPIC:
                return await self._call_anthropic(prompt, config, system_message)
            elif config.provider == ModelProvider.GEMINI:
                return await self._call_gemini(prompt, config, system_message)
            elif config.provider == ModelProvider.PERPLEXITY:
                return await self._call_perplexity(prompt, config, system_message)
            elif config.provider == ModelProvider.OLLAMA:
                return await self._call_ollama(prompt, config, system_message)
            else:
                return f"[MOCK COMPLETION for {config.model_id}]: {prompt[:50]}..."
        except Exception as e:
            logger.error(f"LLM Call failed for {provider_name}: {e}")
            # Fallback to a tiny mock rather than crashing the system
            return f"[FALLBACK MOCK]: Service {provider_name} unavailable."
        finally:
            # 3. Report usage for tracking
            self.governor.report_usage(provider_name)

    async def _call_openai(self, prompt, config, system):
        """Call OpenAI API via OpenAIClient"""
        from services.ai.openai_client import get_openai_client
        
        client = get_openai_client()
        
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await client.chat_completion(
                messages=messages,
                model=config.model_id,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            return response.content
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
            # Fallback to GPT-3.5 if GPT-4 fails
            if config.model_id.startswith("gpt-4"):
                logger.info("Falling back to GPT-3.5-turbo")
                try:
                    response = await client.chat_completion(
                        messages=messages,
                        model="gpt-3.5-turbo",
                        temperature=config.temperature,
                        max_tokens=config.max_tokens
                    )
                    return response.content
                except Exception as fallback_error:
                    logger.error(f"GPT-3.5 fallback also failed: {fallback_error}")
            raise

    async def _call_anthropic(self, prompt, config, system):
        # Implementation would use anthropic SDK
        logger.info(f"Routing to Anthropic: {config.model_id}")
        return f"Anthropic Response for: {prompt[:30]}"

    async def _call_gemini(self, prompt, config, system):
        # Implementation would use google-generativeai SDK
        logger.info(f"Routing to Gemini: {config.model_id}")
        return f"Gemini Response for: {prompt[:30]}"

    async def _call_perplexity(self, prompt, config, system):
        # Implementation uses OpenAI-compatible client
        logger.info(f"Routing to Perplexity: {config.model_id}")
        return f"Perplexity Response for: {prompt[:30]}"

    async def _call_ollama(self, prompt, config, system):
        """Call Local LLM via Ollama API."""
        import httpx
        logger.info(f"Routing to Local Ollama: {config.model_id}")
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": config.model_id,
            "prompt": f"{system}\n\nUser: {prompt}",
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json().get("response", "[OLLAMA ERROR: No response]")
            except Exception as e:
                logger.error(f"Ollama call failed: {e}")
                return f"[OLLAMA OFFLINE]: {str(e)}"

# Singleton instance
_model_manager = None

def get_model_manager() -> ModelManager:
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager
