from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from core.config import TELEGRAM_BOT_TOKEN
from handlers.router import route_message


# ==========================================
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🐧 Project Kowalski Online.\n\nReady, Skipper."
    )


# ==========================================
# MESSAGE
# ==========================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        message = update.message.text.strip()

        result = route_message(message)

        await update.message.reply_text(
            result["reply"]
        )

    except Exception as e:

        print("\n========== ERROR ==========")
        print(type(e).__name__)
        print(e)
        print("===========================\n")

        await update.message.reply_text(
            "Something went wrong, Skipper."
        )


# ==========================================
# APP
# ==========================================

app = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .build()
)

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("🐧 Kowalski is listening...")

app.run_polling()