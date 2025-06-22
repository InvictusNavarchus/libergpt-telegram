"""
Utility functions for LiberGPT bot
"""

import time
import html
import logging
from typing import Dict, List, Optional
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter for user messages"""
    
    def __init__(self, max_messages: int = 10, time_window: int = 60):
        self.max_messages = max_messages
        self.time_window = time_window
        self.user_messages: Dict[int, deque] = defaultdict(deque)
    
    def is_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to send a message"""
        now = time.time()
        user_queue = self.user_messages[user_id]
        
        # Remove old messages outside the time window
        while user_queue and now - user_queue[0] > self.time_window:
            user_queue.popleft()
        
        # Check if user has exceeded the limit
        if len(user_queue) >= self.max_messages:
            return False
        
        # Add current message timestamp
        user_queue.append(now)
        return True
    
    def get_remaining_time(self, user_id: int) -> int:
        """Get remaining time in seconds until user can send messages again"""
        if user_id not in self.user_messages:
            return 0
        
        user_queue = self.user_messages[user_id]
        if len(user_queue) < self.max_messages:
            return 0
        
        oldest_message = user_queue[0]
        return max(0, int(self.time_window - (time.time() - oldest_message)))

def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

def truncate_message(text: str, max_length: int = 4096) -> str:
    """Truncate message to fit Telegram's limits"""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at a sentence boundary
    truncated = text[:max_length - 3]
    last_period = truncated.rfind('.')
    last_newline = truncated.rfind('\n')
    
    cut_point = max(last_period, last_newline)
    if cut_point > max_length * 0.8:  # If we can keep 80% of the text
        return truncated[:cut_point + 1] + "..."
    
    return truncated + "..."

def format_error_message(error: Exception) -> str:
    """Format error message for user display"""
    error_messages = {
        "ConnectionError": "🔌 Connection error. Please try again later.",
        "TimeoutError": "⏱️ Request timed out. Please try again.",
        "JSONDecodeError": "📝 Invalid response format. Please try again.",
        "HTTPError": "🌐 Server error. Please try again later.",
    }
    
    error_type = type(error).__name__
    return error_messages.get(error_type, f"❌ An error occurred: {str(error)}")

def sanitize_html(text: str) -> str:
    """Sanitize HTML content for safe display"""
    return html.escape(text)

def setup_logging(debug: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('libergpt.log'),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.INFO)
