# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы и папки из рабочей директории в контейнер
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Инициализируем Alembic и перемещаем alembic.ini внутрь папки alembic
RUN alembic init alembic && mv alembic.ini alembic/alembic.ini

# Указываем команду, которая будет выполняться при запуске контейнера
CMD [ "python", "main.py" ]
