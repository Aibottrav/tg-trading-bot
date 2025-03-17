import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = "7850670334:AAHksGaElDlOZbgrHb0uBo-KZ7wiSuPUV5Y"
WEBHOOK_URL = "https://trading-bot-98kz.onrender.com/{}".format(TOKEN)  # Update this with your Render URL

app = Flask(__name__)

# Initialize the Telegram bot
application = ApplicationBuilder().token(TOKEN).build()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define /start command
async def start(update: Update, context):
    await update.message.reply_text("🚀 AI Trading Bot Connected Boss!")

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
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put(update)
    return "OK", 200

# Set Webhook when script runs
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())
    app.run(host="0.0.0.0", port=10000)
