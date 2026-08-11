"""
=============================================================================
MODULE: CHUNKING.PY
Purpose: Split text into smaller overlapping chunks to prepare for embedding
=============================================================================

INSTRUCTIONS:
1. Create the function split_text_simple() to split text by character count
2. Create the function split_text_by_sentences() to split by sentences (smarter)
3. Create the function split_text_by_paragraphs() to split by paragraphs
4. Create the function add_chunk_metadata() to add metadata to each chunk
5. Create the function prepare_chunks() to combine the above functions
"""

from typing import List, Dict
import re

from app.config import config


# ============================================================================
# STEP 1: SIMPLE TEXT SPLITTING (BY CHARACTER COUNT)
# ============================================================================

def split_text_simple(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    TODO: Split text into chunks based on character count + overlap

    Args:
        text (str): Text to split
        chunk_size (int): Size of each chunk (default from config)
        overlap (int): Overlap size (default from config)

    Returns:
        List[str]: List of chunks

    Example:
        text = "This is a very long text..."
        chunks = split_text_simple(text, chunk_size=100, overlap=20)
        # Output: ["This is a very long text...", "very long text..."]

    Implementation suggestion:
    - Use default values from config if parameters are not provided
    - Loop from 0 to len(text) with steps of (chunk_size - overlap)
    - Extract substrings from the current position to position + chunk_size
    - Add to the list
    - Filter out chunks that are too short (< 50 characters)
    """
    # Start coding here
    pass

# ============================================================================
# STEP 2: SMART TEXT SPLITTING (BY SENTENCES)
# ============================================================================

def split_text_by_sentences(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    TODO: Split text by sentences to ensure no sentence is cut off

    Args:
        text (str): Text to split
        chunk_size (int): Size of each chunk (default from config)
        overlap (int): Overlap size (default from config)

    Returns:
        List[str]: List of chunks

    Example:
        text = "This is sentence 1. This is sentence 2. This is sentence 3."
        chunks = split_text_by_sentences(text, chunk_size=50)
        # Output: ["This is sentence 1. This is sentence 2.", "This is sentence 2. This is sentence 3."]

    Implementation suggestion:
    - Split text into sentences using regex or split('.')
    - Loop to combine sentences so that each chunk does not exceed chunk_size
    - Handle overlap by saving a few sentences from the previous chunk
    - Return the list of chunks

    Suggested regex: r'[.!?]+' to split sentences
    """
    # Start coding here
    pass

# ============================================================================
# STEP 3: SPLIT TEXT BY PARAGRAPHS
# ============================================================================

def split_text_by_paragraphs(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    TODO: Split text by paragraphs to maintain better context

    Args:
        text (str): Text to split
        chunk_size (int): Size of each chunk (default from config)
        overlap (int): Overlap size (default from config)

    Returns:
        List[str]: List of chunks

    Example:
        text = "Paragraph 1\n\nParagraph 2\n\nParagraph 3"
        chunks = split_text_by_paragraphs(text, chunk_size=100)

    Implementation suggestion:
    - Split text using '\n\n' to separate paragraphs
    - Similar to split_text_by_sentences but use paragraphs
    - Combine paragraphs so that each chunk does not exceed chunk_size
    """
    # Start coding here
    pass

# ============================================================================
# STEP 4: ADD METADATA TO EACH CHUNK
# ============================================================================

def add_chunk_metadata(chunks: List[str], source: str, file_name: str) -> List[Dict]:
    """
    TODO: Add metadata to each chunk (chunk_id, source, ...)

    Args:
        chunks (List[str]): List of chunks
        source (str): Data source (file path)
        file_name (str): File name

    Returns:
        List[Dict]: List of dictionaries containing chunks and metadata

    Example output:
        [
            {
                "chunk_id": 0,
                "text": "Chunk content 1...",
                "source": "./data/uploads/file.pdf",
                "file_name": "file.pdf",
                "length": 150
            },
            {
                "chunk_id": 1,
                "text": "Chunk content 2...",
                "source": "./data/uploads/file.pdf",
                "file_name": "file.pdf",
                "length": 145
            }
        ]

    Implementation suggestion:
    - Loop through chunks with enumerate to get the index
    - Create a dictionary for each chunk with information: chunk_id, text, source, file_name
    - Add other useful information (length, created_at...)
    - Return the list of dictionaries
    """
    # Start coding here
    pass

# ============================================================================
# STEP 5: COMBINE - PREPARE CHUNKS
# ============================================================================

def prepare_chunks(text: str, source: str, file_name: str, method: str = "simple") -> List[Dict]:
    """
    TODO: Combine the above functions to prepare all chunks

    Args:
        text (str): Text to process
        source (str): File path (source)
        file_name (str): File name
        method (str): Text splitting method ("simple", "sentence", "paragraph")
                     default: "simple"

    Returns:
        List[Dict]: List of chunks with metadata

    Process:
    1. Choose the text splitting method based on the 'method' parameter
    2. Split text into chunks
    3. Add metadata to each chunk
    4. Return the list of chunks

    Suggested code:
    if method == "simple":
        chunks = split_text_simple(text)
    elif method == "sentence":
        chunks = split_text_by_sentences(text)
    elif method == "paragraph":
        chunks = split_text_by_paragraphs(text)
    else:
        raise ValueError("Invalid method")

    chunks_with_metadata = add_chunk_metadata(chunks, source, file_name)
    return chunks_with_metadata
    """
    # Start coding here
    pass
