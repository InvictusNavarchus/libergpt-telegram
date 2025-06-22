# LiberGPT - Free Telegram AI Bot

A robust Telegram bot that provides free access to AI-powered conversations using a personal API backend.

## Features

- 🤖 **Free AI Chat**: Access to AI-powered conversations without limits
- 🧠 **Conversation Memory**: Remembers last 20 conversations for better context
- ⚡ **Fast Responses**: Optimized for quick response times
- 🛡️ **Rate Limiting**: Built-in protection against spam
- 🔧 **Easy Setup**: Simple configuration and deployment
- 📱 **User-Friendly**: Intuitive commands and interactions
- 🌐 **CORS Support**: Works with proxy for web-based API access

## Commands

- `/start` - Start the bot and get welcome message
- `/help` - Show help message with available commands
- `/status` - Check bot status and API availability
- `/clear` - Clear your conversation memory
- Just send any message to chat with the AI!

## Setup

1. **Clone and Navigate**
   ```bash
   cd /path/to/libergpt
   ```

2. **Create Virtual Environment**
   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   uv install python-telegram-bot aiohttp python-dotenv
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token
   ```

5. **Get Bot Token**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Copy the token to your `.env` file

6. **Run the Bot**
   ```bash
   uv run python main.py
   ```

## Configuration

Edit the `.env` file with your settings:

```env
BOT_TOKEN=your_telegram_bot_token_here
API_BASE_URL=https://api.zpi.my.id/v1/ai/copilot
CORS_PROXY=https://cors.fadel.web.id/
DEBUG=False
MAX_MESSAGE_LENGTH=4096
RATE_LIMIT_MESSAGES=10
RATE_LIMIT_WINDOW=60
```

## Project Structure

```
libergpt/
├── main.py              # Bot entry point
├── src/
│   ├── __init__.py
│   ├── bot.py           # Main bot class
│   ├── handlers.py      # Message handlers
│   ├── api_client.py    # API communication
│   ├── config.py        # Configuration management
│   ├── memory.py        # Conversation memory management
│   └── utils.py         # Utility functions
├── pyproject.toml       # Project dependencies
├── .env.example         # Environment template
└── README.md           # This file
```

## API Integration

The bot uses the LiberGPT Copilot API:
- **Endpoint**: `https://api.zpi.my.id/v1/ai/copilot`
- **Method**: GET with `text` parameter
- **CORS Proxy**: `https://cors.fadel.web.id/` (for browser compatibility)

## Rate Limiting

Built-in rate limiting protects against spam:
- Default: 10 messages per 60 seconds per user
- Configurable via environment variables

## Conversation Memory

The bot includes intelligent conversation memory:
- **Memory Capacity**: Stores last 20 conversations per user
- **Context Awareness**: Uses conversation history for better responses
- **Privacy**: Each user's memory is isolated and private
- **Management**: Use `/clear` command to reset your conversation history
- **Automatic Cleanup**: Old conversations are automatically removed when limit is reached

Memory helps the bot:
- Understand context from previous messages
- Provide more relevant and coherent responses
- Remember your preferences and conversation style
- Maintain continuity in longer discussions

## License

MIT License - feel free to use and modify as needed.

## Support

For issues or questions, please check the API documentation in `api.instructions.md`.
