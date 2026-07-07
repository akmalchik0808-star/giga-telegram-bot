import os
import asyncio
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("8817112781:AAHIkVbADc-33KLR8_BOSBJaLja7oSZQ6OI")
GIGACHAT_KEY = os.getenv("MDE5ZjNiNjMtMWYy Ni03ODY0LWFmNWMtN2VhMGM5NDM yYjc1OjU3MjJkYThILWMxY2MtNGFkMi1iMzQ3LTk0ZTJkZTFkYTY4Zg==)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на GigaChat. Напиши мне что угодно.")

async def giga_chat(prompt: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GIGACHAT_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}]
    }
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.post(url, json=data, headers=headers, timeout=60)
        return r.json()["choices"][0]["message"]["content"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Думаю...")
    answer = await giga_chat(user_text)
    await update.message.reply_text(answer)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен")
    app.run_polling()
