# app/main.py

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# # Load environment variables from .env file for local development
load_dotenv()

from app.agents.tutor_agent import TutorAgent

app = FastAPI(title="AI Tutor Agent API")

# Mount the static files directory to serve HTML, CSS, JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/static")

# Initialize the main Tutor Agent
tutor_agent = TutorAgent()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the main HTML page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_class=JSONResponse)
async def ask_agent(request: Request):
    """
    API endpoint to receive user queries and return the agent's response.
    Expects a JSON payload with a "query" key.
    """
    try:
        data = await request.json()
        query = data.get("query")

        if not query:
            return JSONResponse(status_code=400, content={"error": "Query cannot be empty."})

        # Route the query to the main agent
        response = tutor_agent.route_query(query)
        
        return JSONResponse(content={"response": response})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})

# To run this app locally:
# uvicorn app.main:app --reload