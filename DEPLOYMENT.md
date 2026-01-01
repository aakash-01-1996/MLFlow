# MLFlow Deployment Guide

This guide covers multiple ways to deploy your MLFlow project.

---

## Quick Start: Local Docker Deployment

### Prerequisites

- Docker & Docker Compose installed
- Port 5000 available

### Deploy MLFlow Tracking Server

```bash
# Build and start the MLFlow server
docker-compose up -d mlflow-server

# View logs
docker-compose logs -f mlflow-server

# Access MLFlow UI at http://localhost:5000
```

### Stop Services

```bash
docker-compose down
```

---

## Option 1: Docker Deployment (Recommended)

### Start MLFlow Tracking Server

```bash
docker-compose up -d mlflow-server
```

Access the UI at: **http://localhost:5000**

### Serve a Model (After Training)

```bash
# First, train a model and register it
python 20_model_registry.py

# Then serve it using MLFlow
mlflow models serve \
  --model-uri "models:/CustomModel/1" \
  --host 0.0.0.0 \
  --port 5001 \
  --no-conda
```

---

## Option 2: Cloud Deployment

### AWS (Using ECR + ECS/EKS)

1. **Push to ECR:**

```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t mlflow-server .
docker tag mlflow-server:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/mlflow-server:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/mlflow-server:latest
```

2. **Use S3 for artifact storage** (production recommended):

```bash
mlflow server \
  --backend-store-uri postgresql://user:pass@host:5432/mlflow \
  --default-artifact-root s3://your-bucket/mlartifacts \
  --host 0.0.0.0 \
  --port 5000
```

### Google Cloud (GCP)

```bash
# Build with Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT/mlflow-server

# Deploy to Cloud Run
gcloud run deploy mlflow-server \
  --image gcr.io/YOUR_PROJECT/mlflow-server \
  --platform managed \
  --port 5000 \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
# Build and push to Azure Container Registry
az acr build --registry <registry-name> --image mlflow-server:latest .

# Deploy to ACI
az container create \
  --resource-group myResourceGroup \
  --name mlflow-server \
  --image <registry-name>.azurecr.io/mlflow-server:latest \
  --ports 5000 \
  --dns-name-label mlflow-demo
```

---

## Option 3: Kubernetes Deployment

Create the following files for K8s deployment:

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mlflow-server
  template:
    metadata:
      labels:
        app: mlflow-server
    spec:
      containers:
        - name: mlflow-server
          image: your-registry/mlflow-server:latest
          ports:
            - containerPort: 5000
          env:
            - name: MLFLOW_TRACKING_URI
              value: "http://0.0.0.0:5000"
          volumeMounts:
            - name: mlflow-data
              mountPath: /app/mlruns
      volumes:
        - name: mlflow-data
          persistentVolumeClaim:
            claimName: mlflow-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: mlflow-service
spec:
  selector:
    app: mlflow-server
  ports:
    - port: 5000
      targetPort: 5000
  type: LoadBalancer
```

Apply with:

```bash
kubectl apply -f deployment.yaml
```

---

## Option 4: Managed MLFlow Services

### Databricks (Managed MLFlow)

If you're using Databricks, they provide a fully managed MLFlow:

```python
import mlflow
mlflow.set_tracking_uri("databricks")
```

### AWS SageMaker

SageMaker has native MLFlow integration for model tracking.

### Azure ML

Azure Machine Learning supports MLFlow tracking natively.

---

## Production Best Practices

### 1. Use PostgreSQL for Backend Store

```bash
pip install psycopg2-binary

mlflow server \
  --backend-store-uri postgresql://user:password@host:5432/mlflow \
  --default-artifact-root s3://bucket/artifacts \
  --host 0.0.0.0
```

### 2. Enable Authentication

Use a reverse proxy (nginx) with authentication:

```nginx
location / {
    auth_basic "MLFlow";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:5000;
}
```

### 3. Environment Variables

```bash
export MLFLOW_TRACKING_URI=http://your-server:5000
export MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

---

## Testing Your Deployment

After deployment, test with:

```python
import mlflow

# Point to your deployed server
mlflow.set_tracking_uri("http://your-server:5000")

# Create an experiment
experiment_id = mlflow.create_experiment("test-deployment")

# Log a run
with mlflow.start_run(experiment_id=experiment_id):
    mlflow.log_param("test", "value")
    mlflow.log_metric("accuracy", 0.95)

print("Deployment working!")
```

---

## Model Serving Endpoints

Once you've trained and registered a model, serve it:

```bash
# Serve a registered model
mlflow models serve \
  --model-uri "models:/RandomForestRegressor/Production" \
  --host 0.0.0.0 \
  --port 5001

# Or serve from a run
mlflow models serve \
  --model-uri "runs:/<run-id>/model" \
  --host 0.0.0.0 \
  --port 5001
```

Make predictions:

```bash
curl -X POST http://localhost:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["input"], "data": [[15]]}}'
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Production Setup                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Training   │───▶│   MLFlow     │───▶│   Model      │  │
│  │   Scripts    │    │   Server     │    │   Registry   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                             │                    │          │
│                             ▼                    ▼          │
│                      ┌──────────────┐    ┌──────────────┐  │
│                      │  PostgreSQL  │    │  S3/GCS/     │  │
│                      │  (metadata)  │    │  Azure Blob  │  │
│                      └──────────────┘    │  (artifacts) │  │
│                                          └──────────────┘  │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │   Model      │◀───│   Model      │                      │
│  │   Serving    │    │   Registry   │                      │
│  │   (REST API) │    │              │                      │
│  └──────────────┘    └──────────────┘                      │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                          │
│  │  Applications│                                          │
│  │  (inference) │                                          │
│  └──────────────┘                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Commands Reference

| Action             | Command                                                 |
| ------------------ | ------------------------------------------------------- |
| Start local server | `docker-compose up -d`                                  |
| View UI            | `http://localhost:5000`                                 |
| Stop server        | `docker-compose down`                                   |
| Build image        | `docker build -t mlflow-server .`                       |
| Serve model        | `mlflow models serve --model-uri "models:/ModelName/1"` |
| Run experiment     | `python <script>.py`                                    |
