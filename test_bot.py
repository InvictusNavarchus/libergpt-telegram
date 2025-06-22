#!/usr/bin/env python3
"""
Test script for LiberGPT bot components
"""

import sys
import asyncio
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_api_client():
    """Test the API client functionality"""
    print("🧪 Testing API Client...")
    
    from src.api_client import LiberGPTAPIClient
    
    api_client = LiberGPTAPIClient(
        base_url="https://api.zpi.my.id/v1/ai/copilot",
        cors_proxy="https://cors.fadel.web.id/"
    )
    
    try:
        async with api_client as client:
            # Test health check
            is_healthy = await client.health_check()
            print(f"   API Health: {'✅ Healthy' if is_healthy else '❌ Unhealthy'}")
            
            if is_healthy:
                # Test a simple query
                response = await client.get_response("Say hello!")
                print(f"   Test Response: {response[:100]}...")
                print("✅ API Client test passed!")
            else:
                print("⚠️  API appears to be down")
                
    except Exception as e:
        print(f"❌ API Client test failed: {e}")

def test_rate_limiter():
    """Test the rate limiter"""
    print("\n🧪 Testing Rate Limiter...")
    
    from src.utils import RateLimiter
    
    rate_limiter = RateLimiter(max_messages=3, time_window=60)
    
    # Test normal usage
    user_id = 12345
    
    # Should allow first 3 messages
    for i in range(3):
        allowed = rate_limiter.is_allowed(user_id)
        print(f"   Message {i+1}: {'✅ Allowed' if allowed else '❌ Blocked'}")
        if not allowed:
            print("❌ Rate limiter test failed - should allow first 3 messages")
            return
    
    # Should block 4th message
    allowed = rate_limiter.is_allowed(user_id)
    if allowed:
        print("❌ Rate limiter test failed - should block 4th message")
        return
    
    remaining = rate_limiter.get_remaining_time(user_id)
    print(f"   4th Message: ❌ Blocked (wait {remaining}s)")
    print("✅ Rate Limiter test passed!")

def test_utils():
    """Test utility functions"""
    print("\n🧪 Testing Utilities...")
    
    from src.utils import truncate_message, format_error_message
    
    # Test message truncation
    long_message = "A" * 5000
    truncated = truncate_message(long_message, 100)
    
    if len(truncated) <= 100:
        print("   ✅ Message truncation works")
    else:
        print("   ❌ Message truncation failed")
        return
    
    # Test error formatting
    error = ConnectionError("Test error")
    formatted = format_error_message(error)
    
    if "Connection error" in formatted:
        print("   ✅ Error formatting works")
    else:
        print("   ❌ Error formatting failed")
        return
    
    print("✅ Utilities test passed!")

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing Configuration...")
    
    # Create a temporary .env file for testing
    env_content = """
BOT_TOKEN=test_token_123
API_BASE_URL=https://api.example.com
CORS_PROXY=https://cors.example.com
DEBUG=True
MAX_MESSAGE_LENGTH=2048
RATE_LIMIT_MESSAGES=5
RATE_LIMIT_WINDOW=30
    """
    
    with open(".env.test", "w") as f:
        f.write(env_content.strip())
    
    # Temporarily replace the .env file
    import os
    original_env = os.environ.copy()
    
    try:
        # Clear relevant env vars
        for key in ["BOT_TOKEN", "API_BASE_URL", "CORS_PROXY", "DEBUG"]:
            if key in os.environ:
                del os.environ[key]
        
        # Set test env file
        os.environ["DOTENV_PATH"] = ".env.test"
        
        from src.config import Config
        
        # This will fail because we're using a test token
        # But we just want to check if the config loads properly
        try:
            config = Config()
            print("   ❌ Config test failed - should reject test token")
        except ValueError as e:
            if "BOT_TOKEN" in str(e):
                print("   ✅ Config validation works")
            else:
                print(f"   ❌ Unexpected validation error: {e}")
    
    finally:
        # Restore environment
        os.environ.clear()
        os.environ.update(original_env)
        
        # Clean up test file
        if os.path.exists(".env.test"):
            os.remove(".env.test")

async def main():
    """Run all tests"""
    print("🚀 LiberGPT Bot Component Tests")
    print("================================\n")
    
    # Test components
    test_rate_limiter()
    test_utils()
    test_config()
    await test_api_client()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
