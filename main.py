import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Initialize Flask app
app = Flask(__name__)

# Get bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# Enable async handling in Flask
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def handle_update():
    update_data = request.get_json()
    print("Received Update:", update_data)  # Debugging
    
    update = Update.de_json(update_data, bot)

    if "message" in update_data:
        chat_id = update_data["message"]["chat"]["id"]
        text = update_data["message"]["text"]
        await bot.send_message(chat_id, f"Received: {text}")  # Fix: Use `await` properly
    
    # Process update in the Telegram bot application
    await application.update_queue.put(update)

    return "OK", 200

# Start Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

