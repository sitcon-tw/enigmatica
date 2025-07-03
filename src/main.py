from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from command import start, ans, debug, button_callback, stories, view_story_callback, incomplete_story_callback
from utils import get_data

load_dotenv(dotenv_path=Path('.env'))
load_dotenv(dotenv_path=Path('.env.local'), override=True)

def main():
    print('Loading environment variables...')
    app = ApplicationBuilder().token(getenv('BOT_TOKEN')).build()

    print('Initializing bot...')
    get_data.init()
    print('Bot initialized successfully.')

    print('Setting up command handlers...')
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ans", ans))
    app.add_handler(CommandHandler("stories", stories))
    # app.add_handler(CommandHandler("debug", debug))
    app.add_handler(CallbackQueryHandler(lambda update, context: (
        view_story_callback(update, context) if update.callback_query.data.startswith('view_story_')
        else incomplete_story_callback(update, context) if update.callback_query.data.startswith('incomplete_story_')
        else button_callback(update, context)
    )))

    print('Bot starting...')
    app.run_polling()


if __name__ == "__main__":
    main()
