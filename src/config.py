"""
Configuration management for LiberGPT bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.API_BASE_URL = os.getenv("API_BASE_URL", "https://api.zpi.my.id/v1/ai/copilot")
        self.CORS_PROXY = os.getenv("CORS_PROXY", "https://cors.fadel.web.id/")
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))
        self.RATE_LIMIT_MESSAGES = int(os.getenv("RATE_LIMIT_MESSAGES", "10"))
        self.RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
        self.MEMORY_CONVERSATIONS = int(os.getenv("MEMORY_CONVERSATIONS", "20"))
        
        self._validate_config()
    
    def _validate_config(self):
        """Validate required configuration values"""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required. Please set it in your .env file")
        
        if not self.API_BASE_URL:
            raise ValueError("API_BASE_URL is required. Please set it in your .env file")
    
    @property
    def full_api_url(self):
        """Get the full API URL with CORS proxy if configured"""
        if self.CORS_PROXY:
            return f"{self.CORS_PROXY.rstrip('/')}/{self.API_BASE_URL}"
        return self.API_BASE_URL
