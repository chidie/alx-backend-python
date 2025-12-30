FROM python:3.12-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

# Run Django development server (persistent process)
# CMD ["python", "messaging_app/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python", "Django-Middleware-0x03/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "Django-signals_orm-0x04/manage.py", "runserver", "0.0.0.0:8000"]
