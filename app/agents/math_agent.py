# app/agents/math_agent.py

import os
import google.generativeai as genai
from app.tools.calculator import calculator
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
genai.configure(api_key=GEMINI_API_KEY)

class MathAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[calculator] # Provide the calculator tool to the model
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def solve(self, query: str) -> str:
        """
        Solves a math-related query using the Gemini model and the calculator tool.
        """
        # Add a clear instruction for the model
        prompt = f"""
        You are a specialized math tutor. Your task is to solve the following math problem: "{query}".
        
        Follow these steps:
        1.  Analyze the user's query.
        2.  If the query requires a calculation, you MUST use the provided `calculator` tool. Do not perform calculations manually.
        3.  Explain the steps you took to solve the problem.
        4.  Provide a clear and final answer.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while processing your request with the Math Agent: {e}"

# Example of how the agent can be used:
if __name__ == '__main__':
    # You need to set the GOOGLE_API_KEY environment variable to run this
    if not GEMINI_API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
    else:
        math_agent = MathAgent()
        # This query will trigger the calculator tool
        result = math_agent.solve("If a box has 5 apples and I buy 3 more boxes, but then eat 2 apples, how many apples are left? The expression should be (5*4) - 2.")
        print(result)