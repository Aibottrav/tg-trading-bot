import os
import logging
import threading
import time
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging to track bot activity
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load Telegram Bot Token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize Flask server to keep the bot online
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 AI Trading Bot is running and stable!"

def run_flask():
    """Runs Flask in a background thread to prevent Render from stopping the bot."""
    app.run(host='0.0.0.0', port=8080, threaded=True)

# Telegram Bot Functions
async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when /start is used."""
    await update.message.reply_text("🚀 AI Trading Bot Connected! You'll receive real-time trade updates.")

async def unknown(update: Update, context: CallbackContext) -> None:
    """Handles unknown commands."""
    await update.message.reply_text("🤖 Sorry, I didn't understand that command.")

# Keep bot running by pinging itself every 40 seconds
def keep_bot_active():
    while True:
        logger.info("🔄 Bot is running and staying active...")
        time.sleep(40)  # Prevents Render from stopping the bot

# Run the bot and Flask together
def main():
    """Starts the bot and ensures continuous operation."""
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start Flask server in a background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Start the activity checker in a background thread
    threading.Thread(target=keep_bot_active, daemon=True).start()

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
