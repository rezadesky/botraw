FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if any (none needed for now)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# THE HACK: Maneuver around Highrise SDK's old typing-extensions pin
RUN pip install --no-cache-dir tortoise-orm aiosqlite httpx loguru python-dotenv
RUN pip install --no-cache-dir highrise-bot-sdk==24.1.0 --no-deps
RUN pip install --no-cache-dir aiohttp cattrs click pendulum quattro
RUN pip install --no-cache-dir typing-extensions>=4.12.2 --upgrade

# Copy the rest of the application
COPY . .

# Ensure database directory exists
RUN mkdir -p database

# Explicitly copy instances (including .env files)
COPY instances /app/instances

# Copy the python runner script
COPY runner.py .

# Use runner.py as the entrypoint command.
CMD ["python", "runner.py"]
