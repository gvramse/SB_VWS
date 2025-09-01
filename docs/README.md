# 🚀 Kubernetes Hello World - Complete Guide

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Step-by-Step Guide](#step-by-step-guide)
- [Project Structure](#project-structure)
- [Kubernetes Manifests](#kubernetes-manifests)
- [Application Code](#application-code)
- [Deployment Options](#deployment-options)
- [Monitoring & Troubleshooting](#monitoring--troubleshooting)
- [Advanced Examples](#advanced-examples)

## 🌟 Overview

This project provides a complete, production-ready example of deploying a Node.js application to Kubernetes. It includes:

- ✅ **Complete Application**: Node.js Express server with health checks
- ✅ **Docker Containerization**: Multi-stage Dockerfile with security best practices
- ✅ **Kubernetes Manifests**: Deployment, Service, Ingress, ConfigMap, and Namespace
- ✅ **Documentation**: Step-by-step guide with troubleshooting
- ✅ **Interactive HTML Guide**: Visual tutorial with copy-paste commands

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### Required Tools

1. **Kubernetes Cluster**
   - Minikube (local development)
   - Docker Desktop Kubernetes
   - Kind (local cluster)
   - Cloud provider (GKE, EKS, AKS)

2. **kubectl CLI**
   ```bash
   # macOS
   brew install kubectl
   
   # Linux
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   chmod +x kubectl
   sudo mv kubectl /usr/local/bin/
   ```

3. **Docker**
   ```bash
   # macOS
   brew install --cask docker
   
   # Linux
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

### Verify Installation

```bash
kubectl version --client
kubectl cluster-info
docker --version
```

## 🚀 Quick Start

### 1. Clone and Navigate

```bash
cd kubernetes_examples
```

### 2. Build and Deploy

```bash
# Build the Docker image
cd examples
docker build -t kubernetes-hello-world:latest .

# Deploy to Kubernetes
cd ../k8s-manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Access the application
kubectl port-forward service/hello-world-service 8080:80
```

### 3. View the Application

Open http://localhost:8080 in your browser to see the Hello World application running in Kubernetes!

## 📖 Step-by-Step Guide

### Step 1: Create the Application

The application is a simple Node.js Express server that displays system information:

```javascript
// examples/app.js
const express = require('express');
const os = require('os');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send(`
    <h1>🚀 Hello World from Kubernetes!</h1>
    <p>Hostname: ${os.hostname()}</p>
    <p>Platform: ${os.platform()}</p>
    <p>Architecture: ${os.arch()}</p>
    <p>Uptime: ${Math.floor(os.uptime() / 60)} minutes</p>
    <p>Memory: ${Math.round(os.freemem() / 1024 / 1024)} MB free</p>
    <p>Timestamp: ${new Date().toISOString()}</p>
  `);
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

### Step 2: Containerize with Docker

```dockerfile
# examples/Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
USER nodejs
EXPOSE 3000
CMD ["npm", "start"]
```

### Step 3: Create Kubernetes Manifests

#### Namespace
```yaml
# k8s-manifests/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: hello-world
```

#### Deployment
```yaml
# k8s-manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: hello-world
        image: kubernetes-hello-world:latest
        ports:
        - containerPort: 3000
```

#### Service
```yaml
# k8s-manifests/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world-service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: hello-world
```

### Step 4: Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s-manifests/namespace.yaml

# Deploy application
kubectl apply -f k8s-manifests/deployment.yaml
kubectl apply -f k8s-manifests/service.yaml

# Check status
kubectl get pods -n hello-world
kubectl get services -n hello-world
```

### Step 5: Access the Application

```bash
# Port forward to access locally
kubectl port-forward service/hello-world-service 8080:80 -n hello-world

# Or use NodePort/LoadBalancer for external access
kubectl patch service hello-world-service -n hello-world -p '{"spec":{"type":"NodePort"}}'
```

## 📁 Project Structure

```
kubernetes_examples/
├── hello_world.html          # Interactive HTML guide
├── k8s-manifests/            # Kubernetes manifests
│   ├── namespace.yaml       # Namespace definition
│   ├── configmap.yaml       # Configuration
│   ├── deployment.yaml      # Application deployment
│   ├── service.yaml         # Service definition
│   └── ingress.yaml         # Ingress configuration
├── examples/                # Application code
│   ├── app.js              # Node.js application
│   ├── package.json        # Dependencies
│   └── Dockerfile          # Container definition
└── docs/                   # Documentation
    └── README.md           # This file
```

## ⚙️ Kubernetes Manifests

### Deployment Features

- **Replicas**: 3 instances for high availability
- **Resource Limits**: CPU and memory constraints
- **Health Checks**: Liveness and readiness probes
- **Security**: Non-root user execution
- **Environment Variables**: Configurable via ConfigMap

### Service Features

- **ClusterIP**: Internal service discovery
- **Load Balancing**: Automatic traffic distribution
- **Port Mapping**: 80 → 3000 port translation

### Ingress Features

- **Host-based Routing**: `hello-world.local`
- **SSL Termination**: HTTPS support (optional)
- **Path Rewriting**: Clean URL handling

## 💻 Application Code

### Key Features

- **Health Endpoint**: `/health` for Kubernetes probes
- **System Information**: Hostname, platform, memory, etc.
- **Graceful Shutdown**: SIGTERM/SIGINT handling
- **Environment Configuration**: Via ConfigMap
- **Beautiful UI**: Modern CSS styling

### Health Check Endpoint

```javascript
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: Math.floor(process.uptime()),
    environment: config.NODE_ENV
  });
});
```

## 🚀 Deployment Options

### Local Development

```bash
# Minikube
minikube start
minikube addons enable ingress

# Docker Desktop
# Enable Kubernetes in Docker Desktop settings
```

### Cloud Deployment

```bash
# Google Cloud (GKE)
gcloud container clusters create hello-world-cluster
gcloud container clusters get-credentials hello-world-cluster

# AWS (EKS)
eksctl create cluster --name hello-world-cluster
eksctl get cluster --name hello-world-cluster
```

## 📊 Monitoring & Troubleshooting

### Useful Commands

```bash
# Check deployment status
kubectl get deployments -n hello-world
kubectl describe deployment hello-world-deployment -n hello-world

# Check pods
kubectl get pods -n hello-world
kubectl logs -l app=hello-world -n hello-world
kubectl describe pod <pod-name> -n hello-world

# Check services
kubectl get services -n hello-world
kubectl get endpoints -n hello-world

# Monitor resources
kubectl top pods -n hello-world
kubectl top nodes
```

### Common Issues

1. **Image Pull Errors**
   ```bash
   # For local images in Minikube
   eval $(minikube docker-env)
   docker build -t kubernetes-hello-world:latest .
   ```

2. **Port Forward Issues**
   ```bash
   # Check if service exists
   kubectl get services -n hello-world
   
   # Test service connectivity
   kubectl run test --image=busybox -it --rm --restart=Never -- wget -O- hello-world-service:80 -n hello-world
   ```

3. **Pod Startup Issues**
   ```bash
   # Check pod events
   kubectl describe pod <pod-name> -n hello-world
   
   # Check pod logs
   kubectl logs <pod-name> -n hello-world
   ```

## 🔧 Advanced Examples

### With Database

```yaml
# PostgreSQL deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: "myapp"
        - name: POSTGRES_PASSWORD
          value: "password"
```

### With Persistent Storage

```yaml
# Persistent Volume Claim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### With Horizontal Pod Autoscaler

```yaml
# HPA for automatic scaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hello-world-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hello-world-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 🎯 Success Checklist

- ✅ Application builds and runs locally
- ✅ Docker image builds successfully
- ✅ Kubernetes cluster is accessible
- ✅ Deployment creates pods successfully
- ✅ Service exposes application internally
- ✅ Port forwarding works correctly
- ✅ Application responds on health checks
- ✅ Logs show no errors
- ✅ Resource usage is within limits

## 📚 Additional Resources

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Node.js Production Best Practices](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)

---

**🎉 Congratulations! You've successfully deployed a Hello World application to Kubernetes!**

For the interactive HTML guide, open `hello_world.html` in your browser for a visual, step-by-step tutorial with copy-paste commands.

