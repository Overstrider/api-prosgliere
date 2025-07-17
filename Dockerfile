FROM python:3.13-slim

WORKDIR /app

# Install curl for healthchecks and postgresql dependencies
RUN apt-get update && apt-get install -y curl libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
COPY entrypoint-test.sh /entrypoint-test.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /entrypoint-test.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 