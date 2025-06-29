from telegram import Update
from telegram.ext import ContextTypes

async def ans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('This is `ans` command')
