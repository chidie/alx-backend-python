FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

# Run Django development server (persistent process)
# CMD ["python", "messaging_app/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python", "Django-Middleware-0x03/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "Django-signals_orm-0x04/manage.py", "runserver", "0.0.0.0:8000"]
