def analyze_text(text: str) -> str:
    """Analyzes the input text and returns statistics.

    Args:
        text: The input string to analyze.

    Returns:
        A string containing the word count, character count, and line count.
    """
    words = len(text.split())
    chars = len(text)
    lines = len(text.splitlines())
    return f"Words: {words}, Characters: {chars}, Lines: {lines}"
