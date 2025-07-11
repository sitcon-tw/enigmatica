from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
import random

from utils import get_data

chats = {}
active_messages = {}
user_sessions = {}

async def ans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chats
    
    user = update.effective_user
    
    def get_story_number_from_password(text: str):
        for i in get_data.data:
            if get_data.data[i] == text:
                return i
        return None

    if len(context.args) == 0:
        print(f"User {user.username or user.first_name} (ID: {user.id}) used /ans command - no password provided")
        return await update.message.reply_text('你的東西勒?')
    
    answer = ' '.join(context.args)
    story_number = get_story_number_from_password(answer)
    
    if story_number is None:
        print(f"User {user.username or user.first_name} (ID: {user.id}) used /ans command - wrong password: '{answer}'")
    else:
        print(f"User {user.username or user.first_name} (ID: {user.id}) used /ans command - correct password: '*****' -> story {story_number}")
    
    if story_number is None:
        no_story = [
            "「打錯了，請再來一次，還是腦袋也出 bug 了」-- OsGa",
            "「真的沒有人可以理解我嗎......」-- 康喔",
            "「真相就藏在每一個線索中。」-- Denny",
            "「每一則訊息的背後，都藏著說不出口的故事。」-- 橘子",
            "「只要相信就做得到。」-- 柴柴",
            "「為甚麼沒有約我去吃海底撈!!!」-- Ricky",
            "「獻出心臟，找出真相吧。」-- windless",
            "「只要想做，全世界總有人幫你達成。」-- 咪路"
            ]
        return await update.message.reply_text(random.choice(no_story) + "\n(你輸入的東西肯定錯了)")

    chat_id = update.effective_chat.id
    
    story_parts = await get_data.get_story(story_number)
    
    if not story_parts or len(story_parts) == 0:
        return await update.message.reply_text('故事內容是空的欸')
    
    if chat_id in active_messages:
        try:
            await context.bot.edit_message_text(
                text="❌ 已過期",
                chat_id=chat_id,
                message_id=active_messages[chat_id]
            )
        except:
            pass
    
    story_title = get_data.story[story_number]['title']
    user_sessions[chat_id] = user
    chats[chat_id] = {
        'user': user,
        'story_parts': story_parts,
        'current_index': 0,
        'displayed_text': f"📚 {story_title}\n\n{story_parts[0]}" if len(story_parts) > 0 else f"📚 {story_title}\n\n",
        'story_number': story_number
    }
    
    if len(story_parts) > 1:
        progress = f"({1}/{len(story_parts)})"
        keyboard = [
            [InlineKeyboardButton(f"下一個 {progress}", callback_data=f'next_{chat_id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [
            [InlineKeyboardButton("點我完成故事", callback_data=f'done_{chat_id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await update.message.reply_text(
        chats[chat_id]['displayed_text'],
        reply_markup=reply_markup
    )
    active_messages[chat_id] = message.message_id

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chats
    
    query = update.callback_query
    chat_id = update.effective_chat.id
    
    await query.answer()
    
    if chat_id not in chats:
        await query.edit_message_text("❌ 已過期")
        return
    
    chat_data = chats[chat_id]
    callback_data = query.data
    
    if callback_data.startswith('next_'):
        chat_data['current_index'] += 1
        current_idx = chat_data['current_index']
        story_parts = chat_data['story_parts']
        
        if current_idx < len(story_parts):
            chat_data['displayed_text'] += '\n' + story_parts[current_idx]
            
            if current_idx + 1 < len(story_parts):
                progress = f"({current_idx + 1}/{len(story_parts)})"
                keyboard = [
                    [InlineKeyboardButton(f"下一個 {progress}", callback_data=f'next_{chat_id}')]
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("點我完成故事", callback_data=f'done_{chat_id}')]
                ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await query.edit_message_text(
                    text=chat_data['displayed_text'],
                    reply_markup=reply_markup
                )
            except BadRequest as e:
                if "Message is not modified" not in str(e):
                    print(f"Error editing message: {e}")
                # Silently ignore "Message is not modified" errors
        else:
            keyboard = [
                [InlineKeyboardButton("點我完成故事", callback_data=f'done_{chat_id}')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            except BadRequest as e:
                if "Message is not modified" not in str(e):
                    print(f"Error editing message reply markup: {e}")
                # Silently ignore "Message is not modified" errors
            
    elif callback_data.startswith('done_'):
        final_text = chat_data['displayed_text'] + '\n\n✨ 故事完成 ✨'
        
        try:
            await query.edit_message_text(text=final_text)
        except BadRequest as e:
            if "Message is not modified" not in str(e):
                print(f"Error editing final message: {e}")
            # Silently ignore "Message is not modified" errors
        
        user = update.effective_user
        story_number = chat_data['story_number']
        story_title = get_data.story[story_number]['title']
        print(f"User {user.username or user.first_name} (ID: {user.id}) completed story {story_number}: '{story_title}'")
        
        await save_completed_story(user, chat_data['story_number'])
        
        # Log all completed stories for this user
        completed_stories = await get_user_completed_stories(user)
        completed_titles = [get_data.story[s]['title'] for s in completed_stories if s in get_data.story]
        print(f"User {user.username or user.first_name} (ID: {user.id}) has completed {len(completed_stories)} stories: {completed_titles}")
        
        if chat_id in chats:
            del chats[chat_id]
        if chat_id in active_messages:
            del active_messages[chat_id]
        if chat_id in user_sessions:
            del user_sessions[chat_id]

async def save_completed_story(user, story_number):
    import json
    import os
    
    user_data_file = 'src/data/user_data.json'
    
    try:
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        else:
            user_data = {}
        
        user_key = str(user.id)
        if user_key not in user_data:
            user_data[user_key] = {
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'completed_stories': []
            }
        else:
            user_data[user_key]['user_info'] = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        
        if story_number not in user_data[user_key]['completed_stories']:
            user_data[user_key]['completed_stories'].append(story_number)
        
        with open(user_data_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error saving user data: {e}")

async def get_user_completed_stories(user):
    import json
    import os
    
    user_data_file = 'src/data/user_data.json'
    
    try:
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            
            user_key = str(user.id)
            if user_key in user_data:
                return user_data[user_key].get('completed_stories', [])
        
        return []
    except Exception as e:
        print(f"Error loading user data: {e}")
        return []