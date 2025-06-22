"""
Memory management for LiberGPT Telegram bot
Handles conversation history storage and retrieval
"""

import logging
from typing import Dict, List, Tuple, Optional
from collections import deque
from datetime import datetime

logger = logging.getLogger(__name__)

class ConversationMemory:
    """Manages conversation history for users"""
    
    def __init__(self, max_conversations: int = 20):
        """
        Initialize conversation memory
        
        Args:
            max_conversations: Maximum number of conversations to remember per user
        """
        self.max_conversations = max_conversations
        # Dictionary mapping user_id to deque of conversations
        self._conversations: Dict[int, deque] = {}
        logger.info(f"ConversationMemory initialized with max {max_conversations} conversations per user")
    
    def add_conversation(self, user_id: int, user_message: str, bot_response: str) -> None:
        """
        Add a conversation pair to memory
        
        Args:
            user_id: Telegram user ID
            user_message: Message sent by user
            bot_response: Response from bot
        """
        if user_id not in self._conversations:
            self._conversations[user_id] = deque(maxlen=self.max_conversations)
        
        conversation = {
            'timestamp': datetime.now(),
            'user_message': user_message,
            'bot_response': bot_response
        }
        
        self._conversations[user_id].append(conversation)
        logger.debug(f"Added conversation for user {user_id}. Total: {len(self._conversations[user_id])}")
    
    def get_conversation_history(self, user_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        Get conversation history for a user
        
        Args:
            user_id: Telegram user ID
            limit: Maximum number of conversations to return (None for all)
            
        Returns:
            List of conversation dictionaries
        """
        if user_id not in self._conversations:
            return []
        
        conversations = list(self._conversations[user_id])
        
        if limit is not None:
            conversations = conversations[-limit:]
        
        return conversations
    
    def get_context_string(self, user_id: int, include_last_n: int = 5) -> str:
        """
        Get conversation history as a formatted context string
        
        Args:
            user_id: Telegram user ID
            include_last_n: Number of recent conversations to include
            
        Returns:
            Formatted context string
        """
        conversations = self.get_conversation_history(user_id, limit=include_last_n)
        
        if not conversations:
            return ""
        
        context_parts = []
        for conv in conversations:
            context_parts.append(f"User: {conv['user_message']}")
            context_parts.append(f"Assistant: {conv['bot_response']}")
        
        context = "\n".join(context_parts)
        return f"Previous conversation context:\n{context}\n\nCurrent message:"
    
    def clear_user_memory(self, user_id: int) -> int:
        """
        Clear all conversations for a specific user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Number of conversations cleared
        """
        if user_id not in self._conversations:
            return 0
        
        count = len(self._conversations[user_id])
        del self._conversations[user_id]
        logger.info(f"Cleared {count} conversations for user {user_id}")
        return count
    
    def get_memory_stats(self, user_id: int) -> Dict:
        """
        Get memory statistics for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dictionary with memory statistics
        """
        if user_id not in self._conversations:
            return {
                'conversation_count': 0,
                'oldest_conversation': None,
                'newest_conversation': None
            }
        
        conversations = self._conversations[user_id]
        return {
            'conversation_count': len(conversations),
            'oldest_conversation': conversations[0]['timestamp'] if conversations else None,
            'newest_conversation': conversations[-1]['timestamp'] if conversations else None
        }
    
    def get_total_stats(self) -> Dict:
        """
        Get total memory statistics across all users
        
        Returns:
            Dictionary with total statistics
        """
        total_conversations = sum(len(convs) for convs in self._conversations.values())
        active_users = len(self._conversations)
        
        return {
            'active_users': active_users,
            'total_conversations': total_conversations,
            'max_conversations_per_user': self.max_conversations
        }
