from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

TOKEN = os.environ.get("BOT_TOKEN")

def get_metar(icao):
    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw"
    r = requests.get(url)
    if r.status_code == 200 and r.text.strip():
        return r.text.strip()
    else:
        return "METAR not available."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()

    if len(text) == 4 and text.isalpha():
        metar = get_metar(text)
        await update.message.reply_text(metar)
    else:
        await update.message.reply_text(
            "Send a 4-letter ICAO code (example: MRPV)"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✈️ Fly and Learn METAR bot running...")
app.run_polling()
