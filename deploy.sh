#!/bin/bash

# 🚀 Kubernetes Hello World Deployment Script
# This script automates the deployment of the Hello World application to Kubernetes

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check kubectl
    if ! command_exists kubectl; then
        print_error "kubectl is not installed. Please install it first."
        exit 1
    fi
    
    # Check docker
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    # Check if kubectl can connect to cluster
    if ! kubectl cluster-info >/dev/null 2>&1; then
        print_error "Cannot connect to Kubernetes cluster. Please ensure your cluster is running."
        exit 1
    fi
    
    print_success "Prerequisites check passed!"
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image..."
    
    if [ ! -f "examples/Dockerfile" ]; then
        print_error "Dockerfile not found in examples directory"
        exit 1
    fi
    
    cd examples
    docker build -t kubernetes-hello-world:latest .
    cd ..
    
    print_success "Docker image built successfully!"
}

# Function to deploy to Kubernetes
deploy_to_k8s() {
    print_status "Deploying to Kubernetes..."
    
    # Create namespace
    print_status "Creating namespace..."
    kubectl apply -f k8s-manifests/namespace.yaml
    
    # Apply ConfigMap
    print_status "Applying ConfigMap..."
    kubectl apply -f k8s-manifests/configmap.yaml
    
    # Apply Deployment
    print_status "Applying Deployment..."
    kubectl apply -f k8s-manifests/deployment.yaml
    
    # Apply Service
    print_status "Applying Service..."
    kubectl apply -f k8s-manifests/service.yaml
    
    # Wait for deployment to be ready
    print_status "Waiting for deployment to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/hello-world-deployment -n hello-world
    
    print_success "Deployment completed successfully!"
}

# Function to check deployment status
check_status() {
    print_status "Checking deployment status..."
    
    echo ""
    echo "=== Pods ==="
    kubectl get pods -n hello-world
    
    echo ""
    echo "=== Services ==="
    kubectl get services -n hello-world
    
    echo ""
    echo "=== Deployment ==="
    kubectl get deployment hello-world-deployment -n hello-world
    
    echo ""
    echo "=== Endpoints ==="
    kubectl get endpoints -n hello-world
}

# Function to show access information
show_access_info() {
    print_success "Deployment completed! Here's how to access your application:"
    echo ""
    echo "🌐 To access the application:"
    echo "   kubectl port-forward service/hello-world-service 8080:80 -n hello-world"
    echo "   Then open http://localhost:8080 in your browser"
    echo ""
    echo "📊 To monitor the application:"
    echo "   kubectl logs -l app=hello-world -n hello-world"
    echo "   kubectl get pods -n hello-world"
    echo ""
    echo "🔧 To troubleshoot:"
    echo "   kubectl describe deployment hello-world-deployment -n hello-world"
    echo "   kubectl describe service hello-world-service -n hello-world"
}

# Function to cleanup
cleanup() {
    print_status "Cleaning up deployment..."
    
    kubectl delete namespace hello-world --ignore-not-found=true
    
    print_success "Cleanup completed!"
}

# Function to show help
show_help() {
    echo "🚀 Kubernetes Hello World Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  deploy      Deploy the application to Kubernetes"
    echo "  status      Check the deployment status"
    echo "  cleanup     Remove the deployment"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Deploy the application"
    echo "  $0 status    # Check status"
    echo "  $0 cleanup  # Remove deployment"
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        check_prerequisites
        build_image
        deploy_to_k8s
        check_status
        show_access_info
        ;;
    "status")
        check_status
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac

