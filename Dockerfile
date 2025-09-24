# Базовый образ Python 3.11
FROM python:3.13

FROM python:3.13

WORKDIR /app

COPY /requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

COPY . .

# Команда для старта приложения (используем Uvicorn как ASGI-сервер)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
