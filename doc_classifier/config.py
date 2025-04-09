import os
from pathlib import Path

# Base directories
HOME_DIR = str(Path.home())
BASE_DIR = os.path.join(HOME_DIR, 'Documents', 'Ministry_Docs')

# Document categories
DOCUMENT_CATEGORIES = [
    'Application',
    'Report', 
    'Complaint',
    'Memo',
    'Letter',
    'Invoice'
]

# File type mappings
FILE_TYPE_MAPPINGS = {
    '.pdf': 'OCR',
    '.png': 'OCR',
    '.jpg': 'OCR',
    '.jpeg': 'OCR',
    '.doc': 'Word',
    '.docx': 'Word',
    '.xls': 'Excel',
    '.xlsx': 'Excel',
    '.ppt': 'PowerPoint',
    '.pptx': 'PowerPoint',
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.mp4': 'Video',
    '.avi': 'Video',
    '.mov': 'Video',
    '.jpg': 'Image',
    '.jpeg': 'Image',
    '.png': 'Image',
    '.gif': 'Image'
}

# Kaggle settings
KAGGLE_DATASET = 'zimbabwe-ministry-docs/documents'  # Example dataset
KAGGLE_DATA_DIR = os.path.join(BASE_DIR, 'kaggle_data')

# Model settings
MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'models', 'classifier.pkl')
VECTORIZER_SAVE_PATH = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')

# Logging settings
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'doc_classifier.log')
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# OCR settings
TESSERACT_CONFIG = {
    'psm': 6,  # Assume a single uniform block of text
    'oem': 3,  # Default OCR engine mode
    'timeout': 30  # Seconds per page
}

# Image preprocessing settings
PREPROCESSING = {
    'resize_width': 1200,
    'threshold_method': 'otsu',
    'denoise': True
}
