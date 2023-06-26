import telebot

from controllers.task_controller import TaskController
from db.database import Database


class TaskBot:
    def __init__(self, bot_token, db_url):
        self.bot = telebot.TeleBot(bot_token)
        self.db = Database(db_url)
        self.controller = TaskController(self.bot, self.db)

    def start(self):
        self.controller.register_handlers()
        self.bot.polling()

    def close(self):
        self.db.close()
