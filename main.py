from flask import Flask, request
import os
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Make sure this is set
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def handle_update():
    update_data = request.get_json()
    print("Received Update:", update_data)  # Debugging

    update = Update.de_json(update_data, bot)

    # Ensure async handling
    if "message" in update_data:
        chat_id = update_data["message"]["chat"]["id"]
        text = update_data["message"]["text"]
        await bot.send_message(chat_id=chat_id, text=f"Received: {text}")  # Add await

    await application.update_queue.put(update)  # Add await

    return "OK", 200

if __name__ == "__main__":
    app.run(port=10000, debug=True)
