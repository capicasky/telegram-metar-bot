import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =====================
# CONFIG
# =====================
TOKEN = os.environ.get("BOT_TOKEN")

# =====================
# COMMANDS
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Fly and Learn — METAR & TAF Bot\n"
        "By Casky 🧑‍✈️\n\n"
        "📌 How to use:\n"
        "• Send ICAO code → METAR\n"
        "  Example: MRPV\n"
        "• Send: TAF MRPV\n\n"
        "Commands:\n"
        "/start – Welcome\n"
        "/help – Help\n"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧭 Fly and Learn — Help\n\n"
        "METAR:\n"
        "• Send 4-letter ICAO code\n"
        "  Example: MRPV\n\n"
        "TAF:\n"
        "• Send: TAF + ICAO\n"
        "  Example: TAF MRPV\n\n"
        "More features coming soon ✈️\n"
        "— Casky"
    )

# =====================
# WEATHER FUNCTIONS
# =====================
def get_metar(icao: str) -> str:
    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw"
    r = requests.get(url)
    if r.status_code == 200 and r.text.strip():
        return f"🌤 METAR {icao}\n{r.text.strip()}"
    return "❌ METAR not available."

def get_taf(icao: str) -> str:
    url = f"https://aviationweather.gov/api/data/taf?ids={icao}&format=raw"
    r = requests.get(url)
    if r.status_code == 200 and r.text.strip():
        return f"🌦 TAF {icao}\n{r.text.strip()}"
    return "❌ TAF not available."

# =====================
# MESSAGE HANDLER
# =====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()

    if text.startswith("TAF "):
        icao = text.replace("TAF ", "").strip()
        if len(icao) == 4 and icao.isalpha():
            await update.message.reply_text(get_taf(icao))
        else:
            await update.message.reply_text("Use: TAF ICAO (example: TAF MRPV)")
        return

    if len(text) == 4 and text.isalpha():
        await update.message.reply_text(get_metar(text))
        return

    await update.message.reply_text(
        "Send ICAO code (MRPV)\n"
        "or: TAF MRPV\n"
        "Use /help for more info"
    )

# =====================
# MAIN
# =====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✈️ Fly and Learn bot v1.1 running — by Casky")
    app.run_polling()

if __name__ == "__main__":
    main()
