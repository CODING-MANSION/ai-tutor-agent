# app/agents/physics_agent.py

import os
import google.generativeai as genai
from app.tools.constants import lookup_physics_constant
from pathlib import Path
from dotenv import load_dotenv

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
genai.configure(api_key=GEMINI_API_KEY)

class PhysicsAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[lookup_physics_constant] # Provide the lookup tool to the model
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def answer(self, query: str) -> str:
        """
        Answers a physics-related query using the Gemini model and the constants lookup tool.
        """
        # Add a clear instruction for the model
        prompt = f"""
        You are a specialized physics tutor. Your task is to answer the following physics question: "{query}".
        
        Follow these steps:
        1.  Analyze the user's query.
        2.  If the query requires the value of a physical constant (like speed of light), you MUST use the `lookup_physics_constant` tool. Do not use hardcoded values.
        3.  Explain the concept clearly and concisely.
        4.  If you used a constant, state its value and unit in your explanation.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while processing your request with the Physics Agent: {e}"

# Example of how the agent can be used:
if __name__ == '__main__':
    # You need to set the GOOGLE_API_KEY environment variable to run this
    if not GEMINI_API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
    else:
        physics_agent = PhysicsAgent()
        # This query will trigger the lookup tool
        result = physics_agent.answer("What is Newton's second law? How would I calculate the force on an object if I knew the speed of light?")
        print(result)