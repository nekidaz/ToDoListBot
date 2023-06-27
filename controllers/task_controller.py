from telebot import TeleBot, types


class TaskController:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.handle_start)
        self.bot.callback_query_handler(func=lambda query: True)(self.handle_callback_query)
        self.bot.message_handler(func=lambda message: True)(self.handle_message)

    def handle_start(self, message):
        try:
            welcome_message = "Привет! Я бот для управления списком задач. Выбери действие из меню:"
            self.db.add_user(username=message.from_user.username, telegram_id=message.from_user.id)
            self.bot.reply_to(message, welcome_message, reply_markup=self.get_main_menu_keyboard())
        except Exception as e:
            self.bot.reply_to(message, f"Произошла ошибка: {str(e)}")

    def get_main_menu_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton('Добавить задачу', callback_data='add'),
            types.InlineKeyboardButton('Список задач', callback_data='list')
        )
        keyboard.row(
            types.InlineKeyboardButton('Удалить задачу', callback_data='delete'),
            types.InlineKeyboardButton('Отметить как выполненное', callback_data='done')
        )
        return keyboard

    def handle_callback_query(self, callback_query):
        try:
            if callback_query.data == 'add':
                self.bot.send_message(callback_query.from_user.id, "Введите задачу:")
                self.bot.register_next_step_handler(callback_query.message, self.handle_add_task)
            elif callback_query.data == 'list':
                self.handle_list(callback_query)
                return
            elif callback_query.data == 'delete':
                self.bot.send_message(callback_query.from_user.id, "Введите номер задачи для удаления:")
                self.bot.register_next_step_handler(callback_query.message, self.handle_delete_task)
            elif callback_query.data == 'done':
                self.bot.send_message(callback_query.from_user.id, "Введите номер задачи для отметки как выполненной:")
                self.bot.register_next_step_handler(callback_query.message, self.handle_mark_on_done)
            self.bot.answer_callback_query(callback_query.id)
        except Exception as e:
            self.bot.send_message(callback_query.from_user.id, f"Произошла ошибка: {str(e)}")

    def handle_add_task(self, message):
        try:
            task = message.text.strip()
            telegram_id = message.from_user.id

            if task:
                self.db.add_task(task, telegram_id)
                self.bot.send_message(message.chat.id, "Задача успешно добавлена!", reply_markup=self.get_main_menu_keyboard())
            else:
                self.bot.send_message(message.chat.id, "Пожалуйста, введите непустую задачу.")
        except Exception as e:
            self.bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

    def handle_list(self, callback_query):
        try:
            telegram_id = callback_query.from_user.id
            tasks = self.db.get_all_tasks(telegram_id=telegram_id)

            if tasks:
                task_list = ""
                for index, task in enumerate(tasks):
                    task_status = "Выполнено" if task.status else "Не выполнено"
                    task_list += f"{index + 1}. {task.title} - {task_status}\n"
                reply_message = f"Список задач:\n{task_list}"
            else:
                reply_message = "У вас нет задач."

            self.bot.send_message(telegram_id, reply_message, reply_markup=self.get_main_menu_keyboard())
        except Exception as e:
            self.bot.send_message(telegram_id, f"Произошла ошибка: {str(e)}")

    def handle_delete_task(self, message):
        try:
            telegram_id = message.from_user.id
            task_index = int(message.text.strip())

            tasks = self.db.get_all_tasks(telegram_id=telegram_id)

            if 1 <= task_index <= len(tasks):
                task = tasks[task_index - 1]
                if self.db.delete_task(task.id):
                    reply_message = f"Задача '{task.title}' успешно удалена."
                else:
                    reply_message = "Ошибка при удалении задачи."
            else:
                reply_message = "Неверный номер задачи."

            self.bot.send_message(message.chat.id, reply_message, reply_markup=self.get_main_menu_keyboard())
        except Exception as e:
            self.bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

    def handle_mark_on_done(self, message):
        try:
            telegram_id = message.from_user.id
            task_index = int(message.text.strip())

            tasks = self.db.get_all_tasks(telegram_id=telegram_id)

            if 1 <= task_index <= len(tasks):
                task = tasks[task_index - 1]
                if self.db.update_task_status(task.id):
                    reply_message = f"Задача '{task.title}' отмечена как выполненная."
                else:
                    reply_message = "Ошибка при обновлении задачи."
            else:
                reply_message = "Неверный номер задачи."

            self.bot.send_message(message.chat.id, reply_message, reply_markup=self.get_main_menu_keyboard())
        except Exception as e:
            self.bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

    def handle_message(self, message):
        if message.content_type == 'text':
            if message.text.startswith('/'):
                command = message.text.split()[0].lower()
                if command == '/add':
                    self.handle_add_task(message)
                elif command == '/delete':
                    self.handle_delete_task(message)
                elif command == '/done':
                    self.handle_mark_on_done(message)
                elif command == "/list":
                    self.handle_list(message)
            else:
                self.bot.send_message(message.chat.id, "Выбери действие из меню:", reply_markup=self.get_main_menu_keyboard())

    def handle(self, message):
        if message.content_type == 'text':
            if message.text.startswith('/'):
                command = message.text.split()[0].lower()
                if command == '/start':
                    self.handle_start(message)
                elif command == '/add':
                    self.handle_add_task(message)
                elif command == '/list':
                    self.handle_list(message)
                elif command == '/delete':
                    self.handle_delete_task(message)
                elif command == '/done':
                    self.handle_mark_on_done(message)
                else:
                    self.bot.send_message(message.chat.id, "Я не понимаю эту команду.")
            else:
                self.handle_message(message)
