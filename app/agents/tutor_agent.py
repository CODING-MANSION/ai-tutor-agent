# app/agents/tutor_agent.py

import os
import google.generativeai as genai
from app.agents.math_agent import MathAgent
from app.agents.physics_agent import PhysicsAgent
from dotenv import load_dotenv
from pathlib import Path

try:
    dotenv_path = Path("app") / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print(f"Warning: .env file not found at {dotenv_path}")
except Exception as e:
    print(f"Error loading .env file: {e}")

# Configure the Gemini API key
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# This check is crucial for early feedback
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    # This will prevent the app from even trying to start without a key
    print("CRITICAL ERROR: GOOGLE_API_KEY is not set. The application cannot function.")


class TutorAgent:
    def __init__(self):
        """
        Initializes the TutorAgent.
        - The classifier model is now configured with a detailed system prompt for accuracy.
        - Specialist agents are initialized.
        """
        if not GEMINI_API_KEY:
            # The agent is initialized but will be in a non-functional state.
            # The routing method will handle returning an error message.
            self.classifier_model = None
            return

        # --- CHANGE 1: Using a more capable model and a much better prompt ---
        # We now use 'gemini-1.5-pro-latest' for classification for better instruction following.
        # The system_instruction provides clear context, rules, and examples (few-shot prompting).
        self.classifier_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="""You are an expert query classifier. Your task is to categorize a user's query into one of three categories: 'math', 'physics', or 'general'.

You must respond with ONLY the category name as a single word in lowercase. Do not add any other text, explanation, or punctuation.

Examples:
- User Query: "Can you help me solve 2x + 5 = 11?"
- Your Response: math

- User Query: "Explain the concept of gravitational force."
- Your Response: physics

- User Query: "what is the best way to learn python"
- Your Response: general
"""
        )
        self.math_agent = MathAgent()
        self.physics_agent = PhysicsAgent()

    def _classify_query(self, query: str) -> str:
        """
        Uses the configured Gemini model to classify the query.
        Now includes robust error handling.
        """
        try:
            # The prompt is now just the query itself, as all instructions are in the model's system prompt.
            response = self.classifier_model.generate_content(query)
            category = response.text.strip().lower()

            # Stricter check for an exact match first
            if category in ["math", "physics", "general"]:
                return category

            # Fallback for cases where the model might still be slightly verbose
            if "math" in category: return "math"
            if "physics" in category: return "physics"
            
            # If the response is unexpected, default to general but log it.
            print(f"[CLASSIFICATION WARNING] Model returned an unexpected category: '{category}'. Defaulting to 'general'.")
            return "general"

        # --- CHANGE 2: Specific and descriptive error handling ---
        except Exception as e:
            # This is the most important change. It will print the actual error to your console.
            print(f"\n--- [TUTOR AGENT ERROR] ---")
            print(f"Failed to classify query due to an API or configuration error.")
            print(f"Query: '{query}'")
            print(f"Error Details: {e}")
            print(f"This is often caused by an invalid or missing GOOGLE_API_KEY in your .env file.")
            print(f"---------------------------\n")
            return "general"

    def route_query(self, query: str) -> str:
        """
        Routes the user's query to the appropriate specialist agent.
        """
        # --- CHANGE 3: Check for API key at the point of use ---
        if not self.classifier_model or not GEMINI_API_KEY:
            return "Error: The Gemini API key is not configured correctly on the server. Please check your `.env` file or server environment variables."

        category = self._classify_query(query)
        
        # This print statement is very helpful for debugging in your terminal
        print(f"Query classified as: '{category}'")

        if category == "math":
            return self.math_agent.solve(query)
        elif category == "physics":
            return self.physics_agent.answer(query)
        else:
            return "I can currently only assist with detailed questions about **Math** and **Physics**. What would you like to know about these subjects?"