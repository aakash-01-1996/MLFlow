# MLFlow Tracking Server + Model Serving
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose MLFlow UI port
EXPOSE 5000

# Default command: Start MLFlow tracking server
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
