# api/index.py

from app.main import app as fastapi_app

# Vercel expects a top-level `app` in this file
app = fastapi_app
