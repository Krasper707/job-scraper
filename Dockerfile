# Dockerfile for Hugging Face Spaces

# Use the official Python slim image for a smaller footprint
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system-level dependencies for Chrome using a separate script
# This keeps the Dockerfile cleaner
COPY install_chrome.sh .
RUN chmod +x install_chrome.sh && ./install_chrome.sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask/Gunicorn will run on (Hugging Face uses 7860 by default)
EXPOSE 7860

# The command to run the application using Gunicorn
# Hugging Face provides the PORT environment variable
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]