import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")

# Validate environment variables
if not BOT_TOKEN or not RENDER_URL:
    raise ValueError("⚠️ Missing BOT_TOKEN or RENDER_URL! Check environment variables.")

# Set webhook URL
WEBHOOK_URL = f"{RENDER_URL}/{BOT_TOKEN}"

# Flask app for webhook
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def handle_update():
    update_data = request.get_json()
    print("Received Update:", update_data)  # Debugging

    # Ensure update_data is valid before processing
    if not update_data:
        return "No update received", 400  # Return error if no data received

    try:
        update = Update.de_json(update_data, bot)
        
        # Try sending an immediate response (for debugging)
        if "message" in update_data:
            chat_id = update_data["message"]["chat"]["id"]
            text = update_data["message"]["text"]
            bot.send_message(chat_id, f"Received: {text}")

        application.update_queue.put(update)

        return "OK", 200

    except Exception as e:
        print("Error processing update:", str(e))  # Debugging
        return f"Error: {str(e)}", 500  # Return error to diagnose issue


async def start(update: Update, context):
    await update.message.reply_text("🚀 AI Trading Bot Connected! You’ll start receiving real-time updates Boss.")

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        webhook_url=WEBHOOK_URL
    )
