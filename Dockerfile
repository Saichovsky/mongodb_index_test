# Use an official lightweight Python image
FROM python:3.12-alpine3.21

# Set working directory inside the container
WORKDIR /app

# Copy requirements (if you have a requirements.txt) or install directly
RUN pip install --upgrade pip && pip install --no-cache-dir pymongo faker

# Copy the seed script into the container
COPY seed_script.py .

# Use a system user account
USER 100

# Default command (can be overridden in docker-compose)
CMD ["python", "seed_script.py"]
