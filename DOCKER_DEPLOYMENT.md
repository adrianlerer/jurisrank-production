# 🐳 JurisRank Docker Deployment Guide

## Quick Start

### 🚀 Option 1: Docker Compose (Recommended)
```bash
# Clone repository
git clone https://github.com/adrianlerer/jurisrank-production.git
cd jurisrank-production

# Start production service
docker-compose up -d

# Check health
curl http://localhost:8000/health

# View logs
docker-compose logs -f jurisrank-api
```

### 🔧 Option 2: Manual Docker Build
```bash
# Build container
docker build -t jurisrank-api:latest .

# Run production container
docker run -d \
  --name jurisrank-production \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  jurisrank-api:latest

# Check status
docker ps
docker logs jurisrank-production
```

## 🛠️ Development Mode

### Start Development Environment
```bash
# Start development service with hot reload
docker-compose --profile dev up -d jurisrank-dev

# Access development API
curl http://localhost:5000/api/v1/status

# View development logs
docker-compose logs -f jurisrank-dev
```

## ⚙️ Configuration Options

### Environment Variables
- `DEV_MODE=1` - Enable development mode with hot reload
- `FLASK_ENV=production|development` - Flask environment
- `FLASK_DEBUG=1` - Enable Flask debug mode (dev only)
- `PYTHONUNBUFFERED=1` - Disable Python output buffering

### Volume Mounts
- `/app/logs` - Application logs (persistent)
- `/app/data` - Database and data files (persistent)
- `/app` - Full application (development only)

## 🏥 Health Monitoring

### Health Check Endpoint
```bash
# Check service health
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "0.3.0",
  "database": "connected"
}
```

### Container Health Status
```bash
# Check Docker health status
docker ps --filter "name=jurisrank"

# View health check logs
docker inspect jurisrank-production | jq '.[0].State.Health'
```

## 🚀 Production Deployment

### Cloud Platform Deployment

#### AWS ECS
```bash
# Tag for ECR
docker tag jurisrank-api:latest your-account.dkr.ecr.region.amazonaws.com/jurisrank-api:latest

# Push to ECR
docker push your-account.dkr.ecr.region.amazonaws.com/jurisrank-api:latest
```

#### Google Cloud Run
```bash
# Tag for GCR
docker tag jurisrank-api:latest gcr.io/your-project/jurisrank-api:latest

# Push to GCR
docker push gcr.io/your-project/jurisrank-api:latest

# Deploy to Cloud Run
gcloud run deploy jurisrank-api \
  --image gcr.io/your-project/jurisrank-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

#### Azure Container Instances
```bash
# Create resource group
az group create --name jurisrank-rg --location eastus

# Deploy container
az container create \
  --resource-group jurisrank-rg \
  --name jurisrank-api \
  --image jurisrank-api:latest \
  --dns-name-label jurisrank-api \
  --ports 8000
```

### Kubernetes Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jurisrank-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: jurisrank-api
  template:
    metadata:
      labels:
        app: jurisrank-api
    spec:
      containers:
      - name: jurisrank-api
        image: jurisrank-api:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

## 🔧 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check container logs
docker logs jurisrank-production

# Check for port conflicts
netstat -tlnp | grep :8000

# Rebuild with no cache
docker build --no-cache -t jurisrank-api:latest .
```

#### Database Issues
```bash
# Reset database
docker exec -it jurisrank-production rm -f /app/bibliography.db
docker restart jurisrank-production
```

#### Permission Issues
```bash
# Fix volume permissions
sudo chown -R 1000:1000 ./logs ./data
```

### Performance Tuning

#### Memory Limits
```bash
# Run with memory limit
docker run -d \
  --name jurisrank-production \
  --memory="512m" \
  --memory-swap="1g" \
  -p 8000:8000 \
  jurisrank-api:latest
```

#### CPU Limits
```bash
# Run with CPU limit
docker run -d \
  --name jurisrank-production \
  --cpus="1.5" \
  -p 8000:8000 \
  jurisrank-api:latest
```

## 📊 Monitoring & Logging

### Container Metrics
```bash
# Monitor resource usage
docker stats jurisrank-production

# Export metrics to file
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" > metrics.log
```

### Log Management
```bash
# View real-time logs
docker logs -f jurisrank-production

# Export logs
docker logs jurisrank-production > jurisrank.log 2>&1

# Log rotation (production)
docker run -d \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  jurisrank-api:latest
```

## 🔐 Security Considerations

### Security Best Practices
- ✅ Non-root user (jurisrank:jurisrank)
- ✅ Minimal base image (python:3.11-slim)
- ✅ No sensitive data in image
- ✅ Health checks enabled
- ✅ Resource limits recommended

### Network Security
```bash
# Run with custom network
docker network create --driver bridge jurisrank-net
docker run -d --network jurisrank-net jurisrank-api:latest
```

### Secrets Management
```bash
# Use Docker secrets (swarm mode)
echo "api-key-value" | docker secret create jurisrank-api-key -
```

## 📋 Maintenance

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Backup
```bash
# Backup volumes
docker run --rm -v jurisrank-production_data:/data \
  -v $(pwd):/backup alpine tar czf /backup/jurisrank-backup.tar.gz -C /data .
```

---

*JurisRank Docker Deployment - Production Ready Containerization*