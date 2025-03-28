import os
import asyncio
from flask import Flask, request
import asyncio
from telegram import Bot, Update
from telegram.ext import Application

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def handle_update():
    update_data = request.get_json()
    print("Received Update:", update_data)

    update = Update.de_json(update_data, bot)

    if "message" in update_data:
        chat_id = update_data["message"]["chat"]["id"]
        text = update_data["message"]["text"]

        # Run async function in sync Flask environment
        asyncio.run(bot.send_message(chat_id=chat_id, text=f"Received: {text}"))

    application.update_queue.put(update)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=10000, debug=True)
