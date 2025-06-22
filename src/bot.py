"""
Main bot class for LiberGPT Telegram bot
"""

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from .config import Config
from .api_client import LiberGPTAPIClient
from .handlers import MessageHandlers
from .utils import RateLimiter, setup_logging

logger = logging.getLogger(__name__)

class LiberGPTBot:
    """Main bot class that orchestrates all components"""
    
    def __init__(self, config: Config):
        """
        Initialize the bot with configuration
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.api_client = LiberGPTAPIClient(
            base_url=config.API_BASE_URL,
            cors_proxy=config.CORS_PROXY
        )
        self.rate_limiter = RateLimiter(
            max_messages=config.RATE_LIMIT_MESSAGES,
            time_window=config.RATE_LIMIT_WINDOW
        )
        self.handlers = MessageHandlers(
            api_client=self.api_client,
            rate_limiter=self.rate_limiter,
            max_message_length=config.MAX_MESSAGE_LENGTH
        )
        self.application = None
    
    def setup_handlers(self):
        """Setup all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("status", self.handlers.status_command))
        
        # Message handler for regular text messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message)
        )
        
        # Error handler
        self.application.add_error_handler(self.handlers.handle_error)
        
        logger.info("All handlers registered successfully")
    
    async def post_init(self, application: Application) -> None:
        """
        Post-initialization hook called after the bot starts
        
        Args:
            application: The Telegram Application instance
        """
        logger.info("Bot initialization completed")
        
        # Test API connection
        async with self.api_client as client:
            if await client.health_check():
                logger.info("API health check passed - bot is ready")
            else:
                logger.warning("API health check failed - bot may not function properly")
    
    async def post_shutdown(self, application: Application) -> None:
        """
        Post-shutdown hook called when the bot stops
        
        Args:
            application: The Telegram Application instance
        """
        logger.info("Bot shutdown completed")
    
    def run(self):
        """Start the bot and run until interrupted"""
        # Setup logging
        setup_logging(self.config.DEBUG)
        
        logger.info("Starting LiberGPT Telegram Bot...")
        logger.info(f"Debug mode: {self.config.DEBUG}")
        logger.info(f"API URL: {self.config.API_BASE_URL}")
        logger.info(f"Rate limit: {self.config.RATE_LIMIT_MESSAGES} msgs/{self.config.RATE_LIMIT_WINDOW}s")
        
        # Create application
        self.application = (
            Application.builder()
            .token(self.config.BOT_TOKEN)
            .post_init(self.post_init)
            .post_shutdown(self.post_shutdown)
            .build()
        )
        
        # Setup handlers
        self.setup_handlers()
        
        # Start the bot
        logger.info("Bot is starting...")
        self.application.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
    
    def stop(self):
        """Stop the bot gracefully"""
        if self.application:
            self.application.stop()
            logger.info("Bot stopped")
