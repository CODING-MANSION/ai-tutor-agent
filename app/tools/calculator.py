# app/tools/calculator.py

import re

def calculator(expression: str) -> str:
    """
    A simple calculator tool that can perform basic arithmetic operations.
    It evaluates a string expression and returns the result as a string.
    
    Args:
        expression (str): The mathematical expression to evaluate. 
                          e.g., "2+3*4", "(10-5)/2"
    
    Returns:
        str: The result of the calculation or an error message.
    """
    try:
        # Security check: only allow safe characters for basic arithmetic
        allowed_chars = "0123456789+-*/(). "
        if not all(char in allowed_chars for char in expression):
            return "Error: Invalid characters in expression. Only numbers and basic operators (+, -, *, /) are allowed."

        # Using eval is generally unsafe, but we've sanitized the input above.
        # For a real production system, a more robust parsing library is recommended.
        result = eval(expression)
        return f"The result of the expression '{expression}' is {result}."
    except Exception as e:
        return f"Error: Could not evaluate the expression. {e}"

# Example of how the tool can be used:
if __name__ == '__main__':
    print(calculator("100 / (5 + 5)"))
    print(calculator("2 * 6 + 3"))