from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Performs a mathematical calculation and returns the result."""
    try:
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"