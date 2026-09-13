from pypdf import PdfReader

def load_pdf(file_path):
    """
    Load a PDF file and return its text content.

    Args:
        file_path (str): The path to the PDF file.  

    Returns:
        str: The text content of the PDF file.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += f"\n ---- Page {reader.pages.index(page) + 1} ---- \n"
            text += page.extract_text()
    return text