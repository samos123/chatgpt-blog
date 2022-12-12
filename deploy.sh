#!/usr/bin/env bash

gcloud run deploy web --update-secrets=DATABASE=database:latest \
    --image gcr.io/golangqna/web:latest --allow-unauthenticated \
    --region=us-west1
