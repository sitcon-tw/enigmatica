from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import get_data
from .ans import get_user_completed_stories

async def stories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    completed_stories = await get_user_completed_stories(chat_id)
    
    if not completed_stories:
        await update.message.reply_text('你還沒有完成任何故事喔！')
        return
    
    keyboard = []
    for story_id in completed_stories:
        if story_id in get_data.story:
            title = get_data.story[story_id]['title']
            keyboard.append([InlineKeyboardButton(
                f"📚 {title}",
                callback_data=f'view_story_{story_id}'
            )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '📖 你已完成的故事：',
        reply_markup=reply_markup
    )

async def view_story_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    story_id = query.data.split('_')[2]
    
    if story_id in get_data.story:
        story_parts = await get_data.get_story(story_id)
        if story_parts:
            full_story = '\n'.join(story_parts)
            title = get_data.story[story_id]['title']
            
            await query.edit_message_text(
                f"📚 {title}\n\n{full_story}\n\n✨ 故事重溫完成 ✨"
            )
        else:
            await query.edit_message_text("無法載入故事內容")
    else:
        await query.edit_message_text("故事不存在")