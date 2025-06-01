# app/main.py

import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load environment variables from .env (local-only; Vercel will use its dashboard vars)
load_dotenv()

from app.agents.tutor_agent import TutorAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="AI Tutor Agent API")

# Mount the static directory so that /static/<filename> serves files from app/static/
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Use Jinja2Templates pointing at the same static folder (where index.html lives)
templates = Jinja2Templates(directory="app/static")

# Initialize the TutorAgent instance
try:
    tutor_agent = TutorAgent()
    logger.info("TutorAgent initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize TutorAgent: {e}")
    # If TutorAgent fails to import or initialize, raise an exception so deployment will fail loudly.
    raise

@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root(request: Request):
    """
    Serves the main HTML page (index.html) from app/static/.
    """
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering index.html: {e}")
        raise HTTPException(status_code=500, detail="Could not load the homepage.")

@app.post("/ask", response_class=JSONResponse, tags=["Query"])
async def ask_agent(request: Request):
    """
    API endpoint to receive user queries and return the agent's response.
    Expects a JSON payload with a 'query' key.
    """
    try:
        body = await request.json()
        query = body.get("query", "").strip()

        if not query:
            logger.warning("Received empty query.")
            raise HTTPException(status_code=400, detail="Query cannot be empty.")

        logger.info(f"Received query: {query}")
        # Use your TutorAgent's routing method to get a response
        response_text = tutor_agent.route_query(query)
        logger.info("Generated response successfully.")
        return JSONResponse(content={"response": response_text})

    except HTTPException:
        # Re-raise HTTP exceptions so they return proper status codes
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /ask endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error.")

# To run locally: uvicorn app.main:app --reload
