from telegram import Update
from telegram.ext import ContextTypes
from utils import get_data

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(f"User {user.username or user.first_name} (ID: {user.id}) used /debug command")
    
    await update.message.reply_text(f"data:\n{get_data.data}\nstory:\n{get_data.story}")
