from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from command import start, ans

load_dotenv(dotenv_path=Path('.env'))
load_dotenv(dotenv_path=Path('.env.local'), override=True)

def main():
    app = ApplicationBuilder().token(getenv('BOT_TOKEN')).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ans", ans))

    print('Bot starting...')
    app.run_polling()


if __name__ == "__main__":
    main()
