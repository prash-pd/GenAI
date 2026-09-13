from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Split the input text into smaller chunks for processing.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk. Default is 1000 characters.
        chunk_overlap (int): The number of overlapping characters between chunks. Default is 200 characters.

    Returns:
        list: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)