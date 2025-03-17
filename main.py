import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Load environment variables (make sure you set these in Render)
TOKEN = os.getenv("BOT_TOKEN")
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")

if not BOT_TOKEN or not RENDER_URL:
    raise ValueError("Missing environment variables! Make sure BOT_TOKEN and RENDER_URL are set.")

WEBHOOK_URL = f"{RENDER_URL}/{BOT_TOKEN}"


app = Flask(__name__)

# Initialize the Telegram bot
application = ApplicationBuilder().token(TOKEN).build()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define /start command
async def start(update: Update, context):
    await update.message.reply_text("🚀 AI Trading Bot is now online!")

# Define message handler
async def handle_message(update: Update, context):
    text = update.message.text
    logger.info(f"Received message: {text}")
    await update.message.reply_text(f"Echo: {text}")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(), application.bot)
        application.update_queue.put(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return "Internal Server Error", 500

# Set Webhook when script starts
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())
    app.run(host="0.0.0.0", port=10000)
