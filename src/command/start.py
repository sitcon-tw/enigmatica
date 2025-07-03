from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
🤖 **故事機器人使用說明**

📖 **主要指令：**
• `/ans <密碼>` - 開始閱讀故事
• `/stories` - 查看已完成的故事
• `/start` - 顯示此幫助訊息
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')
