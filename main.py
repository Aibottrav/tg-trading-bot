from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ApplicationBuilder

import os

# Initialize Flask App
app = Flask(__name__)

# Load Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

# Create Telegram Bot Application
app_builder = ApplicationBuilder().token(TOKEN).build()

# Start Command Handler
async def start(update: Update, context):
    await update.message.reply_text("🚀 AI Trading Bot Connected! You’ll start receiving real-time updates.")

# Handle all incoming Telegram messages
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Process incoming updates from Telegram"""
    update = Update.de_json(request.get_json(), bot)
    app_builder.process_update(update)
    return "OK", 200

# Add Handlers
app_builder.add_handler(CommandHandler("start", start))

# Start Webhook
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
