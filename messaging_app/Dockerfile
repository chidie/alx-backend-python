FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . .
EXPOSE 8000

# Example run command: docker run -p 8000:8000 messaging-app
# CMD ["python", "messaging_app/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python", "Django-Middleware-0x03/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "Django-signals_orm-0x04/manage.py", "runserver", "0.0.0.0:8000"]
