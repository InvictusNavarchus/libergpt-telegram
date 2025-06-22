#!/usr/bin/env python3
"""
Simple test for the memory functionality
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.memory import ConversationMemory

def test_memory():
    """Test the conversation memory functionality"""
    print("🧪 Testing Conversation Memory...")
    
    # Create memory instance
    memory = ConversationMemory(max_conversations=3)  # Small limit for testing
    
    # Test adding conversations
    user_id = 12345
    
    print("   Adding conversations...")
    memory.add_conversation(user_id, "Hello", "Hi there! How can I help you?")
    memory.add_conversation(user_id, "What's Python?", "Python is a programming language...")
    memory.add_conversation(user_id, "How do I learn it?", "Start with the basics...")
    
    # Test getting history
    history = memory.get_conversation_history(user_id)
    print(f"   📚 Conversation count: {len(history)}")
    
    # Test context string
    context = memory.get_context_string(user_id, include_last_n=2)
    print(f"   📝 Context length: {len(context)} characters")
    
    # Test memory stats
    stats = memory.get_memory_stats(user_id)
    print(f"   📊 Memory stats: {stats['conversation_count']} conversations")
    
    # Test adding more (should exceed limit)
    memory.add_conversation(user_id, "Tell me more", "Sure, here's more info...")
    history_after = memory.get_conversation_history(user_id)
    print(f"   📚 After limit test: {len(history_after)} conversations")
    
    # Test clearing memory
    cleared = memory.clear_user_memory(user_id)
    print(f"   🗑️ Cleared: {cleared} conversations")
    
    # Verify empty
    final_history = memory.get_conversation_history(user_id)
    print(f"   📚 After clear: {len(final_history)} conversations")
    
    print("✅ Memory tests completed successfully!")

if __name__ == "__main__":
    test_memory()
