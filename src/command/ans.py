from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils import get_data

chats = {}

async def ans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chats
    
    def get_story_number_from_password(text: str):
        for i in get_data.data:
            if get_data.data[i] == text:
                return i
        return None

    if len(context.args) == 0:
        return await update.message.reply_text('你的東西勒?')
    
    answer = context.args[0]
    story_number = get_story_number_from_password(answer)
    
    if story_number is None:
        return await update.message.reply_text('找不到這個欸')

    chat_id = update.effective_chat.id
    
    story_parts = await get_data.get_story(story_number)
    
    if not story_parts or len(story_parts) == 0:
        return await update.message.reply_text('故事內容是空的欸')
    
    chats[chat_id] = {
        'story_parts': story_parts,
        'current_index': 0,
        'displayed_text': story_parts[0] if len(story_parts) > 0 else ''
    }
    
    if len(story_parts) > 1:
        keyboard = [
            [InlineKeyboardButton("下一個", callback_data=f'next_{chat_id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [
            [InlineKeyboardButton("完成", callback_data=f'done_{chat_id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        chats[chat_id]['displayed_text'],
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chats
    
    query = update.callback_query
    chat_id = update.effective_chat.id
    
    await query.answer()
    
    if chat_id not in chats:
        await query.edit_message_text("故事資料遺失，請重新開始")
        return
    
    chat_data = chats[chat_id]
    callback_data = query.data
    
    if callback_data.startswith('next_'):
        chat_data['current_index'] += 1
        current_idx = chat_data['current_index']
        story_parts = chat_data['story_parts']
        
        if current_idx < len(story_parts):
            chat_data['displayed_text'] += '\n\n' + story_parts[current_idx]
            
            if current_idx + 1 < len(story_parts):
                keyboard = [
                    [InlineKeyboardButton("下一個", callback_data=f'next_{chat_id}')]
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("完成", callback_data=f'done_{chat_id}')]
                ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=chat_data['displayed_text'],
                reply_markup=reply_markup
            )
        else:
            keyboard = [
                [InlineKeyboardButton("完成", callback_data=f'done_{chat_id}')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
            
    elif callback_data.startswith('done_'):
        await query.edit_message_text(
            text=chat_data['displayed_text'] + '\n\n✨ 故事完成 ✨'
        )
        
        # Optional: Clean up chat data
        if chat_id in chats:
            del chats[chat_id]