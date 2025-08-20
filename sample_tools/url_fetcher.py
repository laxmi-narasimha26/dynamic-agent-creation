import requests

def fetch_url(url: str) -> str:
    """Fetches the content of a URL.

    Args:
        url: The URL to fetch.

    Returns:
        The first 500 characters of the content or an error message.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text[:500]
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"
