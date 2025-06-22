#!/bin/bash
# Setup script for LiberGPT Telegram Bot

echo "🤖 LiberGPT Bot Setup"
echo "===================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created! Please edit it with your bot token."
    echo ""
    echo "To get a bot token:"
    echo "1. Message @BotFather on Telegram"
    echo "2. Create a new bot with /newbot"
    echo "3. Copy the token to your .env file"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Check if bot token is set
source .env
if [ "$BOT_TOKEN" = "your_telegram_bot_token_here" ] || [ -z "$BOT_TOKEN" ]; then
    echo "⚠️  Please set your BOT_TOKEN in the .env file before running the bot!"
    echo "   Edit .env and replace 'your_telegram_bot_token_here' with your actual token"
    exit 1
fi

echo "🚀 Setup complete! You can now run the bot with:"
echo "   uv run python main.py"
echo ""
echo "Or activate the virtual environment and run directly:"
echo "   source .venv/bin/activate"
echo "   python main.py"
