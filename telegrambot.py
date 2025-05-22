import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Replace with your real bot token from @BotFather
bot_token = "7621558167:AAFhTABR3sQUNXSU8SCzVOjTj9hFTmIis8I"

# --- Allowed exact phrases ---
allowed_phrases = [
    "Your order has been confirmed in my app. You're in luck! Please send me your transaction QR code to receive your commission immediately. Have a great day!",
    "We’ve successfully sent your commission. Kindly verify the transaction and consider supporting our channel. Your support means a lot to us!"
]

# --- Link check function ---
def contains_exactly_one_link(message: str) -> bool:
    url_pattern = r'https?://[^\s]+'
    links = re.findall(url_pattern, message)
    return len(links) == 1

# --- Allow if exact phrase or one link ---
def is_allowed_message(message: str) -> bool:
    if any(phrase.strip() == message.strip() for phrase in allowed_phrases):
        return True
    return contains_exactly_one_link(message)

# --- Start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send a message with exactly one link or one of the approved messages."
    )

# --- Main filter handler ---
async def filter_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text or ""
    chat_id = message.chat_id
    message_id = message.message_id

    if is_allowed_message(text):
        return  # Allowed ✅
    else:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            print(f"❌ Failed to delete message: {e}")

# --- Main function ---
async def main():
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_message))

    print("✅ Bot is running. Press Ctrl+C to stop.")
    await app.run_polling()

# --- Run the bot ---
if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()  # ✅ FIX for 'event loop is already running'
    asyncio.run(main())
