#!/usr/bin/env python3
"""
LiberGPT Telegram Bot - Main Entry Point

A robust Telegram bot providing free AI-powered conversations
using the LiberGPT Copilot API.
"""

import sys
import signal
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import Config
from src.bot import LiberGPTBot

logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)

def main():
    """Main function to run the bot"""
    try:
        # Load configuration
        config = Config()
        
        # Create and run bot
        bot = LiberGPTBot(config)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start the bot
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
