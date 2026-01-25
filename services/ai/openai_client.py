"""
==============================================================================
FILE: services/ai/openai_client.py
ROLE: OpenAI GPT Integration Client
PURPOSE: Provides GPT-4 chat completions, function calling, and embeddings.
         Used by Autocoder agent, natural language command processor, and
         strategy analysis pipelines.

INTEGRATION POINTS:
    - ModelManager: Registered as OPENAI provider
    - APIGovernor: Rate limiting (3/min, 200/day free tier)
    - AutocoderAgent: Primary consumer for code generation
    - CommandProcessor: Natural language portfolio commands

MODELS SUPPORTED:
    - gpt-4o (default)
    - gpt-4-turbo
    - gpt-3.5-turbo (fallback)

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
import json
from typing import Dict, Any, Optional, List, AsyncIterator
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import openai
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI SDK not installed. Install with: pip install openai")


@dataclass
class TokenUsage:
    """Token usage tracking"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class CompletionResponse:
    """Structured completion response"""
    content: str
    model: str
    usage: TokenUsage
    finish_reason: str = "stop"


class OpenAIClient:
    """
    Client for OpenAI GPT API.
    Supports streaming and non-streaming completions, function calling, and embeddings.
    """
    
    def __init__(self, api_key: Optional[str] = None, mock: bool = False):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
            mock: If True, uses mock responses instead of live API
        """
        self.mock = mock
        self.api_key = api_key
        
        if not mock and OPENAI_AVAILABLE:
            self.client = AsyncOpenAI(api_key=api_key)
        else:
            self.client = None
            if not OPENAI_AVAILABLE:
                logger.warning("OpenAI SDK not available. Using mock mode.")
                self.mock = True
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        functions: Optional[List[Dict]] = None,
        function_call: Optional[str] = None
    ) -> CompletionResponse:
        """
        Generate chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (gpt-4o, gpt-4-turbo, gpt-3.5-turbo)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            functions: Optional list of function definitions for function calling
            function_call: Function calling mode ('auto', 'none', or function name)
            
        Returns:
            CompletionResponse with content and usage
        """
        if self.mock:
            return self._mock_completion(messages, model)
        
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Check API key.")
        
        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            
            if max_tokens:
                kwargs["max_tokens"] = max_tokens
            
            if functions:
                kwargs["functions"] = functions
                kwargs["function_call"] = function_call or "auto"
            
            if stream:
                return await self._stream_completion(**kwargs)
            
            response = await self.client.chat.completions.create(**kwargs)
            
            return CompletionResponse(
                content=response.choices[0].message.content or "",
                model=response.model,
                usage=TokenUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens
                ),
                finish_reason=response.choices[0].finish_reason
            )
            
        except openai.RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI completion: {e}")
            raise
    
    async def _stream_completion(self, **kwargs) -> CompletionResponse:
        """Handle streaming completion"""
        # For now, collect all chunks and return as single response
        # In future, can yield chunks for real-time display
        content_parts = []
        total_usage = TokenUsage()
        
        stream = await self.client.chat.completions.create(stream=True, **kwargs)
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content_parts.append(chunk.choices[0].delta.content)
            
            if chunk.usage:
                total_usage = TokenUsage(
                    prompt_tokens=chunk.usage.prompt_tokens or 0,
                    completion_tokens=chunk.usage.completion_tokens or 0,
                    total_tokens=chunk.usage.total_tokens or 0
                )
        
        return CompletionResponse(
            content="".join(content_parts),
            model=kwargs.get("model", "gpt-4o"),
            usage=total_usage,
            finish_reason="stop"
        )
    
    async def stream_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncIterator[str]:
        """
        Stream completion chunks.
        
        Yields:
            Content chunks as they arrive
        """
        if self.mock:
            # Mock streaming
            mock_content = self._mock_completion(messages, model).content
            for word in mock_content.split():
                await asyncio.sleep(0.05)  # Simulate streaming delay
                yield word + " "
            return
        
        if not self.client:
            raise RuntimeError("OpenAI client not initialized.")
        
        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "stream": True
            }
            
            if max_tokens:
                kwargs["max_tokens"] = max_tokens
            
            stream = await self.client.chat.completions.create(**kwargs)
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error in streaming completion: {e}")
            raise
    
    async def create_embedding(
        self,
        text: str,
        model: str = "text-embedding-ada-002"
    ) -> List[float]:
        """
        Create embedding vector for text.
        
        Args:
            text: Text to embed
            model: Embedding model to use
            
        Returns:
            List of floats representing the embedding vector
        """
        if self.mock:
            # Return mock embedding (1536 dimensions for ada-002)
            import random
            return [random.random() for _ in range(1536)]
        
        if not self.client:
            raise RuntimeError("OpenAI client not initialized.")
        
        try:
            response = await self.client.embeddings.create(
                model=model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise
    
    def validate_function_schema(self, functions: List[Dict]) -> bool:
        """
        Validate function calling schema before submission.
        
        Args:
            functions: List of function definitions
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        required_fields = ["name", "description", "parameters"]
        
        for func in functions:
            if not isinstance(func, dict):
                raise ValueError(f"Function must be a dict, got {type(func)}")
            
            for field in required_fields:
                if field not in func:
                    raise ValueError(f"Function missing required field: {field}")
            
            # Validate parameters schema
            if "parameters" in func:
                params = func["parameters"]
                if not isinstance(params, dict):
                    raise ValueError("Function parameters must be a dict")
                if "type" not in params:
                    raise ValueError("Function parameters must have 'type' field")
        
        return True
    
    def _mock_completion(self, messages: List[Dict[str, str]], model: str) -> CompletionResponse:
        """Generate mock completion for testing"""
        await asyncio.sleep(0.5)  # Simulate API latency
        
        # Extract user message
        user_message = next((m["content"] for m in messages if m["role"] == "user"), "")
        
        mock_content = f"[MOCK OpenAI {model}] Response to: {user_message[:50]}..."
        
        return CompletionResponse(
            content=mock_content,
            model=model,
            usage=TokenUsage(
                prompt_tokens=len(user_message.split()) * 2,  # Rough estimate
                completion_tokens=len(mock_content.split()) * 2,
                total_tokens=0
            ),
            finish_reason="stop"
        )


# Singleton instance
_openai_client: Optional[OpenAIClient] = None


def get_openai_client(api_key: Optional[str] = None, mock: bool = True) -> OpenAIClient:
    """
    Get singleton OpenAI client instance.
    
    Args:
        api_key: OpenAI API key (if None, reads from environment)
        mock: Use mock mode if True
        
    Returns:
        OpenAIClient instance
    """
    global _openai_client
    
    if _openai_client is None:
        from config.environment_manager import get_settings
        settings = get_settings()
        
        # Use provided key or read from environment
        key = api_key or settings.OPENAI_API_KEY
        
        # Default to mock if no key provided
        use_mock = mock or not key or key == "your_openai_api_key_here"
        
        _openai_client = OpenAIClient(api_key=key, mock=use_mock)
        logger.info(f"OpenAI client initialized (mock={use_mock})")
    
    return _openai_client
