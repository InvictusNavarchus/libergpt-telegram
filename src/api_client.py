"""
API client for communicating with LiberGPT Copilot API
"""

import asyncio
import logging
import urllib.parse
from typing import Optional, Dict, Any
import aiohttp

logger = logging.getLogger(__name__)

class LiberGPTAPIClient:
    """Client for interacting with the LiberGPT Copilot API"""
    
    def __init__(self, base_url: str, cors_proxy: Optional[str] = None, timeout: int = 30):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the API
            cors_proxy: CORS proxy URL if needed
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.cors_proxy = cors_proxy.rstrip('/') if cors_proxy else None
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _build_url(self, prompt: str) -> str:
        """
        Build the complete API URL with encoded prompt
        
        Args:
            prompt: The text prompt to send to the API
            
        Returns:
            Complete URL ready for request
        """
        encoded_prompt = urllib.parse.quote(prompt)
        api_url = f"{self.base_url}?text={encoded_prompt}"
        
        if self.cors_proxy:
            return f"{self.cors_proxy}/{api_url}"
        
        return api_url
    
    async def get_response(self, prompt: str) -> str:
        """
        Get AI response for the given prompt
        
        Args:
            prompt: The text prompt to send to the API
            
        Returns:
            AI response text
            
        Raises:
            aiohttp.ClientError: For HTTP-related errors
            ValueError: For invalid API response format
            asyncio.TimeoutError: For request timeout
        """
        if not self.session:
            raise RuntimeError("API client not initialized. Use as async context manager.")
        
        url = self._build_url(prompt)
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'LiberGPT-Telegram-Bot/1.0'
        }
        
        logger.debug(f"Making API request to: {url}")
        
        try:
            async with self.session.get(url, headers=headers) as response:
                # Check if request was successful
                response.raise_for_status()
                
                # Parse JSON response
                data = await response.json()
                
                # Validate response format
                if not isinstance(data, dict):
                    raise ValueError("API response is not a JSON object")
                
                # Check for expected structure
                if data.get("code") != 200:
                    error_msg = data.get("message", data.get("error", "Unknown API error"))
                    raise ValueError(f"API error: {error_msg}")
                
                response_content = data.get("response", {}).get("content")
                if not response_content:
                    raise ValueError("API response missing content field")
                
                logger.debug(f"Received API response: {len(response_content)} characters")
                return response_content
                
        except aiohttp.ClientTimeout:
            logger.error("API request timed out")
            raise asyncio.TimeoutError("API request timed out")
        
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error during API request: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Unexpected error during API request: {e}")
            raise
    
    async def health_check(self) -> bool:
        """
        Check if the API is healthy and responding
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            await self.get_response("Hello")
            return True
        except Exception as e:
            logger.warning(f"API health check failed: {e}")
            return False
