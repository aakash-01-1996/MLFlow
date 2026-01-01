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

# Copy only necessary files (not the full project)
COPY mlflow_utils.py .

# Create directories for data persistence
RUN mkdir -p /app/mlruns /app/mlartifacts

# Expose MLFlow UI port
EXPOSE 5000

# Default command: Start MLFlow tracking server
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "/app/mlartifacts"]
