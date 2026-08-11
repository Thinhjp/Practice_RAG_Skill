"""
=============================================================================
MODULE: DATA_INGESTION.PY
Purpose: Handle file upload and extract text from various file types
=============================================================================

IMPLEMENTATION GUIDE:
1. Create validate_file() function to check file format
2. Create extract_text_from_pdf() to read PDF files
3. Create extract_text_from_txt() to read TXT files
4. Create extract_text_from_docx() to read DOCX files
5. Create save_uploaded_file() to save file to server
6. Create process_uploaded_file() to coordinate the above steps
"""

import os
import shutil
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from pathlib import Path

# TODO: Import additional required libraries
# from PyPDF2 import PdfReader
# import docx

from app.config import config


# ============================================================================
# STEP 1: VALIDATE FILE
# ============================================================================

def validate_file(filename: str) -> bool:
    """
    TODO: Check if the file is in an allowed format
    
    Args:
        filename (str): File name
        
    Returns:
        bool: True if file is valid, False otherwise
        
    Implementation hints:
    - Get file extension (e.g., .pdf, .txt, .docx)
    - Compare with ALLOWED_FILE_TYPES list in config
    - Return True/False accordingly
    """
    # Start coding here
    pass


# ============================================================================
# STEP 2: EXTRACT TEXT FROM PDF
# ============================================================================

def extract_text_from_pdf(file_path: str) -> str:
    """
    TODO: Extract text from PDF file
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        str: All extracted text from PDF
        
    Implementation hints:
    - Use PyPDF2.PdfReader to open file
    - Loop through all pages
    - Use extract_text() to get text from each page
    - Combine all text and return
    - Handle errors if file is corrupted
    """
    # Start coding here
    pass


# ============================================================================
# STEP 3: EXTRACT TEXT FROM TXT
# ============================================================================

def extract_text_from_txt(file_path: str) -> str:
    """
    TODO: Extract text from TXT file
    
    Args:
        file_path (str): Path to TXT file
        
    Returns:
        str: File content
        
    Implementation hints:
    - Open file with utf-8 encoding
    - Read entire content
    - Return text
    - Handle encoding errors if any
    """
    # Start coding here
    pass


# ============================================================================
# STEP 4: EXTRACT TEXT FROM DOCX
# ============================================================================

def extract_text_from_docx(file_path: str) -> str:
    """
    TODO: Extract text from DOCX file (Word Document)
    
    Args:
        file_path (str): Path to DOCX file
        
    Returns:
        str: File content
        
    Implementation hints:
    - Use python-docx library
    - Open document from file_path
    - Loop through paragraphs
    - Extract text from each paragraph
    - Combine and return
    """
    # Start coding here
    pass


# ============================================================================
# STEP 5: INITIALIZE EMBEDDING MODEL
# ============================================================================

def save_uploaded_file(upload_file: UploadFile) -> str:
    """
    TODO: Save uploaded file to UPLOAD_DIR
    
    Args:
        upload_file (UploadFile): File uploaded via HTTP request
        
    Returns:
        str: Full path to saved file
        
    Raises:
        HTTPException: If file is too large or save fails
        
    Implementation hints:
    - Check file size (< MAX_FILE_SIZE)
    - Create UPLOAD_DIR directory if not exists
    - Save file to directory
    - Return file path
    - Raise HTTPException on error
    """
    # Start coding here
    pass


# ============================================================================
# STEP 6: COORDINATE - PROCESS FILE
# ============================================================================

def process_uploaded_file(upload_file: UploadFile) -> Tuple[str, str]:
    """
    TODO: Coordinate the above functions to process uploaded file
    
    Args:
        upload_file (UploadFile): Uploaded file
        
    Returns:
        Tuple[str, str]: (file_path, extracted_text)
        
    Raises:
        HTTPException: If file is invalid or cannot be processed
        
    Procedure:
    1. Validate file (check format)
    2. Save file to server (save_uploaded_file)
    3. Extract text based on file type
    4. Return file path and extracted text
    
    Example code:
    - if not validate_file(...): raise HTTPException
    - file_path = save_uploaded_file(upload_file)
    - if file_path.endswith('.pdf'): text = extract_text_from_pdf(file_path)
    - elif file_path.endswith('.txt'): text = extract_text_from_txt(file_path)
    - ...similar for other file types
    - return file_path, text
    """
    # Start coding here
    pass
