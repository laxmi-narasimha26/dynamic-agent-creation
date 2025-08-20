import json

def validate_json(data: str) -> str:
    """Validates if the input string is valid JSON.

    Args:
        data: The input string to validate.

    Returns:
        'Valid JSON' or an error message.
    """
    try:
        json.loads(data)
        return "Valid JSON"
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"
