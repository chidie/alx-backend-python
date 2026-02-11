#!/usr/bin/env bash

echo "=== Checking if Minikube is installed ==="

if ! command -v minikube >/dev/null 2>&1; then
    echo "Minikube is not installed. Please install Minikube first."
    exit 1
fi

echo "Minikube is installed."

echo "=== Starting Minikube cluster ==="
minikube start

echo "=== Verifying Kubernetes cluster status ==="
kubectl cluster-info

echo "=== Retrieving available pods ==="
kubectl get pods -A

echo "=== Script completed successfully ==="
