#!/usr/bin/env bash

docker build -t gcr.io/golangqna/web:latest .
docker push gcr.io/golangqna/web:latest
gcloud run deploy web --update-secrets=DATABASE=database:latest \
    --image gcr.io/golangqna/web:latest --allow-unauthenticated \
    --region=us-west1
