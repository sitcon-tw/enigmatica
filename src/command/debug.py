from telegram import Update
from telegram.ext import ContextTypes
from utils import get_data

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"data:\n{get_data.data}\nstory:\n{get_data.story}")
