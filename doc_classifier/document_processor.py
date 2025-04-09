import os
import pytesseract
import cv2
import pandas as pd
from pdf2image import convert_from_path
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
from typing import Tuple, Union
from pathlib import Path

class DocumentProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        self.setup_directories()
        
    def setup_directories(self):
        """Create required directory structure"""
        self.base_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'Ministry_Docs')
        self.dirs = {
            'ocr': os.path.join(self.base_dir, 'OCR_Documents'),
            'word': os.path.join(self.base_dir, 'MS_Office_Documents', 'Word'),
            'excel': os.path.join(self.base_dir, 'MS_Office_Documents', 'Excel'),
            'ppt': os.path.join(self.base_dir, 'MS_Office_Documents', 'PowerPoint'),
            'images': os.path.join(self.base_dir, 'Media_Files', 'Images'),
            'audio': os.path.join(self.base_dir, 'Media_Files', 'Audio'),
            'video': os.path.join(self.base_dir, 'Media_Files', 'Video')
        }
        
        for dir_path in self.dirs.values():
            os.makedirs(dir_path, exist_ok=True)
            
    def preprocess_image(self, image_path: str) -> str:
        """Preprocess image for better OCR results"""
        try:
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            return pytesseract.image_to_string(thresh)
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            raise
            
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using OCR"""
        try:
            pages = convert_from_path(pdf_path)
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page)
            return text
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
            
    def classify_document(self, text: str) -> Tuple[str, float]:
        """Classify document text using trained model"""
        try:
            features = self.vectorizer.transform([text])
            prediction = self.classifier.predict(features)
            proba = self.classifier.predict_proba(features).max()
            return prediction[0], proba
        except Exception as e:
            self.logger.error(f"Classification error: {str(e)}")
            raise
            
    def process_file(self, file_path: str) -> dict:
        """Process a single file and return classification results"""
        try:
            file_type = Path(file_path).suffix.lower()
            text = ""
            
            if file_type in ('.png', '.jpg', '.jpeg'):
                text = self.preprocess_image(file_path)
            elif file_type == '.pdf':
                text = self.extract_text_from_pdf(file_path)
            else:
                # Handle other file types (MS Office, media files)
                return self.handle_special_files(file_path)
                
            doc_type, confidence = self.classify_document(text)
            return {
                'file_path': file_path,
                'type': doc_type,
                'confidence': confidence,
                'text': text[:500] + '...' if len(text) > 500 else text
            }
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            raise
            
    def handle_special_files(self, file_path: str) -> dict:
        """Handle non-OCR files (MS Office, media)"""
        file_type = Path(file_path).suffix.lower()
        dest_dir = None
        
        if file_type in ('.doc', '.docx'):
            dest_dir = self.dirs['word']
            file_type = 'Word'
        elif file_type in ('.xls', '.xlsx'):
            dest_dir = self.dirs['excel']
            file_type = 'Excel'
        elif file_type in ('.ppt', '.pptx'):
            dest_dir = self.dirs['ppt']
            file_type = 'PowerPoint'
        elif file_type in ('.jpg', '.jpeg', '.png', '.gif'):
            dest_dir = self.dirs['images']
            file_type = 'Image'
        elif file_type in ('.mp3', '.wav', '.ogg'):
            dest_dir = self.dirs['audio']
            file_type = 'Audio'
        elif file_type in ('.mp4', '.avi', '.mov'):
            dest_dir = self.dirs['video']
            file_type = 'Video'
            
        if dest_dir:
            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
            os.rename(file_path, dest_path)
            
        return {
            'file_path': file_path,
            'type': file_type,
            'confidence': 1.0,
            'text': f"File moved to {dest_dir}"
        }
