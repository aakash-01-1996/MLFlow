#!/bin/sh
# Start MLFlow server with dynamic PORT from Railway/Render
exec mlflow server \
    --host 0.0.0.0 \
    --port ${PORT:-5000} \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root /app/mlartifacts \
    --gunicorn-opts "--workers 1 --timeout 120"
