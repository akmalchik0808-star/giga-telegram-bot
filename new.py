import os
import httpx
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("8817112781:AAGi1M4egUQ21G0LfukTxF9wC1TIQY5XJ7A")
GIGACHAT_KEY = os.getenv("GIGACHAT_KEY")
GIGA_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
URL = f"https://giga-telegram-bot.onrender.com/{8817112781:AAGi1M4egUQ21G0LfukTxF9wC1TIQY5XJ7A}"

app = Flask(__name__)
application = Application.builder().token(8817112781:AAGi1M4egUQ21G0LfukTxF9wC1TIQY5XJ7A).build()

async def ask_giga(message):
    headers = {"Authorization": f"Bearer {GIGACHAT_KEY}", "Content-Type": "application/json"}
    data = {"model": "GigaChat", "messages": [{"role": "system", "content": "Отвечай всегда на русском"}, {"role": "user", "content": message}]}
    async with httpx.AsyncClient(verify=False, timeout=60.0) as client:
        r = await client.post(GIGA_URL, headers=headers, json=data)
        return r.json()["choices"][0]["message"]["content"]

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ai_answer = await ask_giga(update.message.text)
    await update.message.reply_text(ai_answer)

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    application.update_queue.put_nowait(Update.de_json(request.get_json(), application.bot))
    return "ok"

if __name__ == "__main__":
    application.bot.set_webhook(URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
