import os
import zipfile
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.model_selection import train_test_split
from doc_classifier.document_processor import DocumentProcessor
import logging
from typing import Tuple

class KaggleDatasetManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api = KaggleApi()
        self.api.authenticate()
        
    def download_dataset(self, dataset_name: str, output_dir: str) -> str:
        """Download and extract a Kaggle dataset"""
        try:
            self.logger.info(f"Downloading dataset: {dataset_name}")
            self.api.dataset_download_files(
                dataset_name,
                path=output_dir,
                unzip=True
            )
            return os.path.join(output_dir, dataset_name.split('/')[-1])
        except Exception as e:
            self.logger.error(f"Error downloading dataset: {str(e)}")
            raise
            
    def prepare_training_data(self, dataset_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Prepare training data from downloaded dataset"""
        try:
            # Assuming dataset contains CSV with 'text' and 'category' columns
            data = pd.read_csv(os.path.join(dataset_path, 'data.csv'))
            
            # Split into training and test sets
            train, test = train_test_split(
                data,
                test_size=0.2,
                random_state=42,
                stratify=data['category']
            )
            
            return train, test
        except Exception as e:
            self.logger.error(f"Error preparing training data: {str(e)}")
            raise
            
    def train_model(self, processor: DocumentProcessor, train_data: pd.DataFrame):
        """Train the document classification model"""
        try:
            self.logger.info("Training classification model")
            
            # Vectorize text data
            X_train = processor.vectorizer.fit_transform(train_data['text'])
            y_train = train_data['category']
            
            # Train classifier
            processor.classifier.fit(X_train, y_train)
            
            self.logger.info("Model training completed")
        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}")
            raise
            
    def evaluate_model(self, processor: DocumentProcessor, test_data: pd.DataFrame) -> dict:
        """Evaluate model performance on test data"""
        try:
            self.logger.info("Evaluating model performance")
            
            X_test = processor.vectorizer.transform(test_data['text'])
            y_test = test_data['category']
            
            accuracy = processor.classifier.score(X_test, y_test)
            
            self.logger.info(f"Model accuracy: {accuracy:.2%}")
            return {
                'accuracy': accuracy,
                'test_size': len(test_data)
            }
        except Exception as e:
            self.logger.error(f"Error evaluating model: {str(e)}")
            raise
