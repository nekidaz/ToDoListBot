class TaskController:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.handle_start)
        self.bot.message_handler(commands=['add'])(self.handle_add_task)
        self.bot.message_handler(commands=['list'])(self.handle_list)
        self.bot.message_handler(commands=['delete'])(self.handle_delete_task)
        self.bot.message_handler(commands=['done'])(self.handle_mark_on_done)

    def handle_start(self, message):
        try:
            welcome_message = "Привет! Я бот для управления списком задач. Доступные команды:\n" \
                              "/add <задача> - добавить новую задачу\n" \
                              "/done <индекс> - отметить задачу как выполненную\n" \
                              "/list - показать список задач\n" \
                              "/delete <индекс> - удалить задачу"
            self.db.add_user(message.from_user.username, message.from_user.id)
            self.bot.reply_to(message, welcome_message)
        except Exception as e:
            self.bot.reply_to(message, f"Произошла ошибка: {str(e)}")

    def handle_add_task(self, message):
        try:
            task = message.text[5:].strip()  # Extract the task title from the command message and remove leading/trailing spaces
            telegram_id = message.from_user.id

            if task:
                self.db.add_task(task, telegram_id)
                self.bot.reply_to(message, "Задача успешно добавлена!")
            else:
                self.bot.reply_to(message, "Пожалуйста, введите непустую задачу.")
        except Exception:
            self.bot.reply_to(message, "Введите правильно например как тут \n /done 1 ")

    def handle_list(self, message):
        try:
            telegram_id = message.from_user.id
            tasks = self.db.get_all_tasks(telegram_id=telegram_id)

            if tasks:
                task_list = ""
                for index, task in enumerate(tasks):
                    task_status = "Выполнено" if task.status else "Не выполнено"
                    task_list += f"{index + 1}. {task.title} - {task_status}\n"
                reply_message = f"Список задач:\n{task_list}"
            else:
                reply_message = "У вас нет задач."

            self.bot.reply_to(message, reply_message)
        except Exception as e:
            self.bot.reply_to(message, f"Произошла ошибка: {str(e)}")

    def handle_delete_task(self, message):
        try:
            telegram_id = message.from_user.id
            task_index = int(message.text.split("/delete")[1])

            tasks = self.db.get_all_tasks(telegram_id=telegram_id)

            if 1 <= task_index <= len(tasks):
                task = tasks[task_index - 1]
                if self.db.delete_task(task.id):
                    reply_message = f"Задача '{task.title}' успешно удалена."
                else:
                    reply_message = "Ошибка при удалении задачи."
            else:
                reply_message = "Неверный номер задачи."

            self.bot.reply_to(message, reply_message)
        except Exception as e:
            self.bot.reply_to(message, "Введите правильно например как тут \n /delete 1 ")

    def handle_mark_on_done(self, message):
        try:
            telegram_id = message.from_user.id
            task_index = int(message.text.split("/done")[1])

            tasks = self.db.get_all_tasks(telegram_id=telegram_id)

            if 1 <= task_index <= len(tasks):
                task = tasks[task_index - 1]
                if self.db.update_task_status(task.id):
                    reply_message = f"Задача '{task.title}' отмечена как выполненная."
                else:
                    reply_message = "Ошибка при обновлении задачи."
            else:
                reply_message = "Неверный номер задачи."

            self.bot.reply_to(message, reply_message)
        except Exception as e:
            self.bot.reply_to(message, f"Произошла ошибка: {str(e)}")
