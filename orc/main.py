import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Get the directory where this script is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Detect if running in Cloud Run (K_SERVICE env var is automatically set there)
if os.getenv("K_SERVICE"):
    # Cloud Run: writable temp storage
    SESSION_SERVICE_URI = "sqlite:////tmp/sessions.db"
else:
    # Local development: persistent storage in project folder
    SESSION_SERVICE_URI = "sqlite:///./sessions.db"

# Example allowed origins for CORS
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "*"  # Allow all origins (use cautiously in production)
]

# Set web=True if you intend to serve a web interface
SERVE_WEB_INTERFACE = True

# Create FastAPI app from the ADK agent directory
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_SERVICE_URI,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# You can add custom FastAPI routes here if needed
# Example:
# @app.get("/hello")
# async def hello():
#     return {"message": "Hello, World!"}

if __name__ == "__main__":
    # Use the PORT env var set by Cloud Run, default to 8080 locally
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
