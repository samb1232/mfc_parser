FROM python:3.13-slim

WORKDIR /app
COPY . /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ENV FLASK_APP=app.py
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
