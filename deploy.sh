#!/bin/bash

# MLFlow Deployment Script
# Usage: ./deploy.sh [command]
# Commands: local, docker-build, docker-run, serve-model

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv/bin"
MLFLOW_PORT=${MLFLOW_PORT:-5000}
MODEL_PORT=${MODEL_PORT:-5001}

# Check if virtual environment exists
if [ -d "$VENV_PATH" ]; then
    MLFLOW_CMD="$VENV_PATH/mlflow"
else
    MLFLOW_CMD="mlflow"
fi

case "$1" in
  local)
    echo "🚀 Starting MLFlow server locally..."
    "$MLFLOW_CMD" server \
      --backend-store-uri sqlite:///mlflow.db \
      --default-artifact-root ./mlartifacts \
      --host 0.0.0.0 \
      --port $MLFLOW_PORT
    ;;
    
  docker-build)
    echo "🔨 Building Docker image..."
    docker build -t mlflow-server .
    echo "✅ Image built successfully!"
    ;;
    
  docker-run)
    echo "🐳 Running MLFlow in Docker..."
    docker run -d \
      --name mlflow-tracking-server \
      -p $MLFLOW_PORT:5000 \
      -v $(pwd)/mlruns:/app/mlruns \
      -v $(pwd)/mlartifacts:/app/mlartifacts \
      mlflow-server
    echo "✅ MLFlow server running at http://localhost:$MLFLOW_PORT"
    ;;
    
  serve-model)
    if [ -z "$2" ]; then
      echo "❌ Error: Please provide model URI"
      echo "Usage: ./deploy.sh serve-model <model-uri>"
      echo "Example: ./deploy.sh serve-model 'models:/CustomModel/1'"
      exit 1
    fi
    echo "🤖 Serving model: $2"
    "$MLFLOW_CMD" models serve \
      --model-uri "$2" \
      --host 0.0.0.0 \
      --port $MODEL_PORT \
      --no-conda
    ;;
    
  stop)
    echo "🛑 Stopping MLFlow containers..."
    docker stop mlflow-tracking-server 2>/dev/null || true
    docker rm mlflow-tracking-server 2>/dev/null || true
    echo "✅ Stopped!"
    ;;
    
  *)
    echo "MLFlow Deployment Script"
    echo ""
    echo "Usage: ./deploy.sh [command]"
    echo ""
    echo "Commands:"
    echo "  local        - Start MLFlow server locally (without Docker)"
    echo "  docker-build - Build Docker image"
    echo "  docker-run   - Run MLFlow server in Docker"
    echo "  serve-model  - Serve a trained model (requires model-uri argument)"
    echo "  stop         - Stop running Docker containers"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh local"
    echo "  ./deploy.sh docker-build && ./deploy.sh docker-run"
    echo "  ./deploy.sh serve-model 'models:/CustomModel/1'"
    ;;
esac
