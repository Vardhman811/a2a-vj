
gcloud run deploy capital-agent-service --source . --region us-central1 --project adk-short-bot-465311 --allow-unauthenticated --set-env-vars="GOOGLE_CLOUD_PROJECT=adk-short-bot-465311,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=true"


export APP_URL="https://capital-agent-service-328611943961.us-central1.run.app"

curl -X GET "$APP_URL/list-apps"         

curl -X POST "$APP_URL/apps/buyAgent/users/user123/sessions/session123" -H "Content-Type: application/json" -d '{"state": {"preferred_language": "English", "visit_count": 1}}'

curl -X POST "$APP_URL/run_sse" -H "Content-Type: application/json" -d '{"app_name": "buyAgent", "user_id": "user123", "session_id": "session123", "new_message": {"role": "user", "parts": [{"text": "What pizza do you have?"}]}, "streaming": false}'
