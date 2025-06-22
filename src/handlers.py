"""
Message handlers for LiberGPT Telegram bot
"""

import logging
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction, ParseMode

from .api_client import LiberGPTAPIClient
from .utils import truncate_message, format_error_message, escape_markdown
from .memory import ConversationMemory

logger = logging.getLogger(__name__)

class MessageHandlers:
    """Collection of message handlers for the bot"""
    
    def __init__(self, api_client: LiberGPTAPIClient, rate_limiter, memory: ConversationMemory, max_message_length: int = 4096):
        """
        Initialize message handlers
        
        Args:
            api_client: API client instance
            rate_limiter: Rate limiter instance
            memory: Conversation memory instance
            max_message_length: Maximum message length
        """
        self.api_client = api_client
        self.rate_limiter = rate_limiter
        self.memory = memory
        self.max_message_length = max_message_length
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle /start command
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) started the bot")
        
        welcome_message = """
🤖 **Welcome to LiberGPT\\!**

I'm your free AI assistant powered by advanced language models\\. I can help you with:

✨ **Questions & Answers** \\- Ask me anything\\!
📚 **Explanations** \\- Get detailed explanations on topics
💡 **Creative Tasks** \\- Writing, brainstorming, and more
🔧 **Problem Solving** \\- Help with coding, math, and logic

**Commands:**
• `/help` \\- Show this help message
• `/status` \\- Check bot status
• `/clear` \\- Clear conversation memory
• Just send me any message to start chatting\\!

**Note:** This bot has rate limiting to ensure fair usage for everyone\\. I also remember our conversations for better context\\!

Ready to chat? Send me a message\\! 🚀
        """
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle /help command
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        help_message = """
🤖 **LiberGPT Help**

**Available Commands:**
• `/start` \\- Welcome message and introduction
• `/help` \\- Show this help message
• `/status` \\- Check bot and API status
• `/clear` \\- Clear your conversation memory

**How to Use:**
1\\. Simply send me any message or question
2\\. I'll process it and respond with an AI\\-generated answer
3\\. No special formatting needed \\- just type naturally\\!

**Examples:**
• "What is Python programming?"
• "Explain quantum physics"
• "Write a short story about space"
• "Help me with this math problem: 2x \\+ 5 = 15"

**Rate Limits:**
To ensure fair usage, there are rate limits in place\\. If you hit the limit, you'll be notified when you can send messages again\\.

**Tips:**
• Be specific with your questions for better answers
• For code\\-related questions, mention the programming language
• I can help with explanations, creative writing, problem\\-solving, and more\\!
• I remember our conversations for better context
• Use `/clear` to reset conversation memory if needed

Need more help? Just ask me anything\\! 💬
        """
        
        await update.message.reply_text(
            help_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle /status command
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        logger.info(f"Status check requested by user {update.effective_user.id}")
        
        # Show typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )
        
        # Check API health
        async with self.api_client as client:
            api_healthy = await client.health_check()
        
        # Get memory stats
        memory_stats = self.memory.get_memory_stats(update.effective_user.id)
        
        status_emoji = "🟢" if api_healthy else "🔴"
        api_status = "Online" if api_healthy else "Offline"
        
        status_message = f"""
🤖 **LiberGPT Status**

**Bot:** 🟢 Online
**API:** {status_emoji} {api_status}
**Version:** 1\\.0\\.0

**Rate Limiting:**
• Max messages: {self.rate_limiter.max_messages} per {self.rate_limiter.time_window}s
• Your status: {"✅ Available" if self.rate_limiter.is_allowed(update.effective_user.id) else "⏳ Rate limited"}

**Memory:**
• Conversations stored: {memory_stats['conversation_count']}/{self.memory.max_conversations}
• Use `/clear` to reset memory

**Last Updated:** Just now
        """
        
        await update.message.reply_text(
            status_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle regular text messages
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Message from user {user.id} ({user.username}): {message_text[:50]}...")
        
        # Check rate limiting
        if not self.rate_limiter.is_allowed(user.id):
            remaining_time = self.rate_limiter.get_remaining_time(user.id)
            rate_limit_message = f"""
⏳ **Rate Limit Exceeded**

You've sent too many messages recently\\. Please wait **{remaining_time} seconds** before sending another message\\.

This helps ensure fair usage for all users\\. Thank you for understanding\\! 🙏
            """
            
            await update.message.reply_text(
                rate_limit_message,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        
        # Show typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )
        
        try:
            # Get conversation context for better responses
            context_string = self.memory.get_context_string(user.id, include_last_n=3)
            
            # Prepare message with context if available
            if context_string:
                full_message = f"{context_string}\n{message_text}"
            else:
                full_message = message_text
            
            # Get AI response
            async with self.api_client as client:
                ai_response = await client.get_response(full_message)
            
            # Store conversation in memory
            self.memory.add_conversation(user.id, message_text, ai_response)
            
            # Truncate if necessary
            if len(ai_response) > self.max_message_length:
                ai_response = truncate_message(ai_response, self.max_message_length)
                ai_response += "\n\n*[Message truncated due to length]*"
            
            # Send response
            await update.message.reply_text(ai_response)
            
            logger.info(f"Responded to user {user.id} with {len(ai_response)} characters")
            
        except Exception as e:
            logger.error(f"Error processing message from user {user.id}: {e}")
            
            error_message = format_error_message(e)
            await update.message.reply_text(error_message)
    
    async def handle_error(self, update: Optional[Update], context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle errors that occur during message processing
        
        Args:
            update: Telegram update object (may be None)
            context: Bot context
        """
        logger.error(f"Exception while handling an update: {context.error}")
        
        # Try to send error message to user if update is available
        if update and update.effective_chat:
            try:
                error_message = "❌ An unexpected error occurred. Please try again later."
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=error_message
                )
            except Exception as e:
                logger.error(f"Failed to send error message to user: {e}")
    
    async def clear_memory_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle /clear command to clear conversation memory
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        user = update.effective_user
        logger.info(f"Memory clear requested by user {user.id} ({user.username})")
        
        # Clear user's conversation memory
        cleared_count = self.memory.clear_user_memory(user.id)
        
        if cleared_count > 0:
            clear_message = f"""
🗑️ **Memory Cleared\\!**

Successfully cleared **{cleared_count}** conversations from your memory\\.

Your conversation history has been reset\\. I won't remember our previous conversations anymore\\.

You can start fresh by sending me a new message\\! 🚀
            """
        else:
            clear_message = """
🗑️ **Memory Already Empty**

You don't have any conversation history to clear\\.

Start chatting with me and I'll remember our conversations\\! 💬
            """
        
        await update.message.reply_text(
            clear_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
