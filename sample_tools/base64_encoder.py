import base64

def encode_base64(text: str) -> str:
    """Encodes the input text to Base64.

    Args:
        text: The input string to encode.

    Returns:
        The Base64-encoded string.
    """
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')
