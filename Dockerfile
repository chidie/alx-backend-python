FROM python:3.11-alpine

WORKDIR /app/python-generators-0x00
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "0-stream_users.py"]