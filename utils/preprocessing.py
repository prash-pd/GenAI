import re

def clean_text(text: str) -> str:
    """
    Clean the input text by removing unwanted characters and formatting.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text.
    """

    text = text.replace('\n', ' ')  # Replace newlines with spaces  
    # Remove leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace within the text
    text = re.sub(r'\s+', ' ', text)
    return text 