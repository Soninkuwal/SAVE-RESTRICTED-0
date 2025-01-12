FROM python:3.9-slim

WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary port
EXPOSE 8080

# Run the bot
CMD ["python", "bot/main.py"]
