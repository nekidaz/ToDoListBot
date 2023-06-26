import os
from dotenv import load_dotenv

from bot.bot import TaskBot
from db.connectToDB import get_database_url
load_dotenv()

if __name__ == "__main__":
    bot_token = os.getenv("BOT_TOKEN")

    db_url = get_database_url()

    task_bot = TaskBot(bot_token, db_url)
    task_bot.start()
