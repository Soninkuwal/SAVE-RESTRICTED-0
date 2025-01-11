import os

# Environment variables for secure deployment
API_ID = os.getenv("API_ID", "YOUR_API_ID")  # Replace with your Telegram API ID
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")  # Replace with your Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")  # Replace with your bot token
PORT = int(os.getenv("PORT", 8080))  # Default port for deployment environments
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "your_log_channel_id")  # Channel ID for logging
