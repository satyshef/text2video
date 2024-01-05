# Используем базовый образ с Python
FROM python:3.8

# Устанавливаем рабочую директорию
WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

# Копируем зависимости и код приложения
#COPY requirements.txt .
COPY app/ .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Определяем команду запуска приложения
CMD ["python", "app.py"]
