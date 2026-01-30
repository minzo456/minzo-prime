import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from flask import Flask
import threading

# Flask Setup (Render එකට අවශ්‍යයි)
server = Flask(__name__)
@server.route('/')
def health_check(): return "MINZO-PRIME IS ONLINE", 200

# Gemini Config
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Specialist Logic
    prompt = f"You are a secret intelligence specialist. User: {user_text}"
    response = model.generate_content(prompt)
    await update.message.reply_text(response.text)

def run_bot():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    # බෝට් එක Background එකේ දුවවන්න
    threading.Thread(target=run_bot).start()
    # Render එකට අවශ්‍ය Web Port එක පණගන්වන්න
    port = int(os.environ.get("PORT", 5000))
    server.run(host='0.0.0.0', port=port)
