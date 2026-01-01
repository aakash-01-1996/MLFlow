# MLFlow Tracking Server - Optimized for low memory
FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Upgrade pip and install dependencies with memory optimization
COPY requirements-docker.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-docker.txt \
    && rm -rf /root/.cache

# Copy startup script
COPY start.sh .
RUN chmod +x start.sh

# Create directories for data persistence
RUN mkdir -p /app/mlruns /app/mlartifacts

# Railway uses dynamic PORT
ENV PORT=5000
EXPOSE 5000

# Use shell script to handle dynamic PORT
CMD ["./start.sh"]
