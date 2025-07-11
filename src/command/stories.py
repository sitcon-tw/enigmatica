from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import get_data
from .ans import get_user_completed_stories

async def stories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(f"User {user.username or user.first_name} (ID: {user.id}) used /stories command")
    
    completed_stories = await get_user_completed_stories(user)
    
    keyboard = []
    for story_id in get_data.story:
        title = get_data.story[story_id]['title']
        if story_id in completed_stories:
            keyboard.append([InlineKeyboardButton(
                f"📚 {title}",
                callback_data=f'view_story_{story_id}'
            )])
        else:
            keyboard.append([InlineKeyboardButton(
                "❓",
                callback_data=f'incomplete_story_{story_id}'
            )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '📖 所有故事：',
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

async def incomplete_story_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    story_id = query.data.split('_')[2]
    
    if story_id in get_data.story:
        title = get_data.story[story_id]['title']
        await query.edit_message_text(
            f"❓ {title}\n\n這個故事還沒有完成喔！\n使用 /ans 命令和正確的密碼來開始閱讀這個故事。"
        )
    else:
        await query.edit_message_text("故事不存在")