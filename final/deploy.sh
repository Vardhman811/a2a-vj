#!/bin/bash

# Cloud Run deployment script for orchestrator agent

# Configuration - Update these values
PROJECT_ID="adk-short-bot-465311"
SERVICE_NAME="orchestrator-agent"
REGION="us-central1"

# Set environment variables
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
export GOOGLE_CLOUD_LOCATION=$REGION
export GOOGLE_GENAI_USE_VERTEXAI=True

# Deploy using gcloud
echo "Deploying orchestrator agent to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,GOOGLE_GENAI_USE_VERTEXAI=True" \
  --timeout 300s

echo "Deployment complete!"
echo "Service URL: https://$SERVICE_NAME-$REGION.a.run.app"
