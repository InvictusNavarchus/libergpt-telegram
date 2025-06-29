# 🚀 Quick Start Guide - LiberGPT Telegram Bot

## Prerequisites
- Python 3.8+
- Telegram account
- Bot token from @BotFather

## 1. Setup Bot Token

1. **Get Bot Token**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot`
   - Choose a name (e.g., "LiberGPT Assistant")
   - Choose a username (e.g., "libergpt_assistant_bot")
   - Copy the bot token

2. **Configure Environment**:
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env file and replace 'your_telegram_bot_token_here' with your actual token
   nano .env
   ```

## 2. Install Dependencies

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate
uv install python-telegram-bot aiohttp python-dotenv

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install python-telegram-bot aiohttp python-dotenv
```

## 3. Run the Bot

```bash
# Method 1: Using uv (recommended)
uv run python main.py

# Method 2: Using activated venv
source .venv/bin/activate
python main.py

# Method 3: Using setup script
./setup.sh && uv run python main.py
```

## 4. Test the Bot

1. **Find your bot** on Telegram (search for the username you chose)
2. **Start a conversation** with `/start`
3. **Send a test message** like "Hello! How are you?"
4. **Try commands**:
   - `/help` - Show help
   - `/status` - Check status

## 5. Troubleshooting

### Bot doesn't respond
- Check if bot token is correct in `.env`
- Verify bot is running without errors
- Test API with: `uv run python test_bot.py`

### API errors
- Check internet connection
- Verify API endpoints are accessible
- Check logs in `libergpt.log`

### Rate limiting
- Default: 10 messages per 60 seconds per user
- Adjust in `.env`: `RATE_LIMIT_MESSAGES` and `RATE_LIMIT_WINDOW`

## 6. Configuration Options

Edit `.env` file:

```env
# Required
BOT_TOKEN=your_bot_token_here

# API Configuration (usually don't need to change)
API_BASE_URL=https://api.zpi.my.id/v1/ai/copilot

# Optional Settings
DEBUG=False                    # Enable debug logging
MAX_MESSAGE_LENGTH=4096       # Max response length
RATE_LIMIT_MESSAGES=10        # Messages per time window
RATE_LIMIT_WINDOW=60          # Time window in seconds
```

## 7. Running in Production

### Using systemd (Linux)

1. Create service file:
   ```bash
   sudo nano /etc/systemd/system/libergpt-bot.service
   ```

2. Add content:
   ```ini
   [Unit]
   Description=LiberGPT Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=your_username
   WorkingDirectory=/path/to/libergpt
   ExecStart=/path/to/libergpt/.venv/bin/python main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable libergpt-bot
   sudo systemctl start libergpt-bot
   ```

### Using screen/tmux

```bash
# Using screen
screen -S libergpt-bot
uv run python main.py
# Ctrl+A, D to detach

# Using tmux
tmux new-session -d -s libergpt-bot 'uv run python main.py'
```

## 8. Monitoring

- **Logs**: Check `libergpt.log` for bot activity
- **Status**: Use `/status` command in Telegram
- **Health**: Run `uv run python test_bot.py`

## 🎉 You're Ready!

Your LiberGPT bot should now be running and responding to messages on Telegram!
