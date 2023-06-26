from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models.modles import Base, User, Task


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.create_tables()
        self.migrate(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def migrate(self, db_url):
        import os
        from alembic.config import Config
        from alembic import command

        # Получаем абсолютный путь к текущему файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Формируем путь к файлу alembic.ini
        alembic_ini_path = os.path.join(current_dir, "../alembic/alembic.ini")

        # Создаем экземпляр объекта Config и настраиваем его
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", os.path.join(current_dir, "../alembic"))
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)

        # Выполняем миграцию
        command.upgrade(alembic_cfg, "head", sql=False)

    def add_user(self, username, telegram_id):
        existing_user = self.session.query(User).filter_by(telegramid=telegram_id).first()
        if not existing_user:
            user = User(username=username, telegramid=telegram_id)
            self.session.add(user)
            self.session.commit()

    def add_task(self, title, telegram_id):
        user = self.session.query(User).filter_by(telegramid=telegram_id).first()
        if user:
            task = Task(title=title, user_telegramid=telegram_id)
            self.session.add(task)
            self.session.commit()

    def get_all_tasks(self, telegram_id):
        user = self.session.query(User).filter_by(telegramid=telegram_id).first()
        if user:
            tasks = self.session.query(Task).filter_by(user_telegramid=telegram_id).order_by(Task.id).all()
            return tasks
        else:
            return []

    def delete_task(self, task_id):
        task = self.session.query(Task).get(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        else:
            return False

    def update_task_status(self, task_id):
        task = self.session.query(Task).get(task_id)
        if task:
            task.status = True
            self.session.commit()
            return True
        return False

    def close(self):
        self.session.close()
