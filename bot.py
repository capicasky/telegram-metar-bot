from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import requests

TOKEN = "8523983515:AAHzxuZ4FYX_Hi5s3CyxTjwdTeRRtKjAJmE"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Fly and Learn – METAR Bot\n\n"
        "How to use:\n"
        "• Send a 4-letter ICAO code to get METAR\n"
        "• Example: MRPV\n\n"
        "Use /help for more options"
    )
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧭 Fly and Learn – Help\n\n"
        "METAR:\n"
        "• Send a 4-letter ICAO code\n"
        "  Example: MRPV\n\n"
        "Commands:\n"
        "• /start – Welcome message\n"
        "• /help – This help message\n\n"
        "More features coming soon ✈️"
    )
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

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✈️ Fly and Learn METAR bot running...")
app.run_polling()
