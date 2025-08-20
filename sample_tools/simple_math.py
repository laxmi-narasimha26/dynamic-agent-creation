def simple_math(expression: str) -> str:
    """Evaluates a simple math expression.

    Args:
        expression: A simple math expression (e.g., '2 + 2').

    Returns:
        The result of the expression or an error message.
    """
    try:
        # A safer way to evaluate simple math expressions
        return str(eval(expression, {'__builtins__': {}}, {}))
    except Exception as e:
        return f"Error evaluating expression: {e}"
