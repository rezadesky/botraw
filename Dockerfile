# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app/core
COPY core/requirements.txt /app/core/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r core/requirements.txt

# Copy the core directory contents (code) into the container at /app/core
COPY core /app/core

# Copy the rest if needed, or just core is enough if we run from there.
# But we need models and bot.

# Set environment variables to ensure output buffer is flushed
ENV PYTHONUNBUFFERED=1

# Command to run the bot
# We use shell form to allow variable expansion from environment variables provided by docker-compose
CMD highrise core.bot:MyBot $HIGHRISE_ROOM_ID $HIGHRISE_TOKEN
