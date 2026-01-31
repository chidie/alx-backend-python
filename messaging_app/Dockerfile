FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY messaging_app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . .
EXPOSE 8000

# CMD ["python", "messaging_app/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python", "Django-Middleware-0x03/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "Django-signals_orm-0x04/manage.py", "runserver", "0.0.0.0:8000"]
