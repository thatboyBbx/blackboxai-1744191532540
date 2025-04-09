import unittest
import os
import shutil
from pathlib import Path
from doc_classifier.document_processor import DocumentProcessor
from doc_classifier.config import BASE_DIR, FILE_TYPE_MAPPINGS

class TestDocumentProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create test files and directories"""
        cls.test_dir = os.path.join(BASE_DIR, 'test_files')
        os.makedirs(cls.test_dir, exist_ok=True)
        
        # Create test files
        cls.test_files = {
            'pdf': os.path.join(cls.test_dir, 'test.pdf'),
            'image': os.path.join(cls.test_dir, 'test.png'),
            'word': os.path.join(cls.test_dir, 'test.docx'),
            'excel': os.path.join(cls.test_dir, 'test.xlsx')
        }
        
        for file_path in cls.test_files.values():
            Path(file_path).touch()
            
    @classmethod
    def tearDownClass(cls):
        """Clean up test files and directories"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
        
    def setUp(self):
        self.processor = DocumentProcessor()
        
    def test_directory_creation(self):
        """Test that required directories are created"""
        for dir_path in self.processor.dirs.values():
            self.assertTrue(os.path.exists(dir_path))
            
    def test_file_processing(self):
        """Test processing of different file types"""
        for file_type, file_path in self.test_files.items():
            result = self.processor.process_file(file_path)
            self.assertIn('type', result)
            self.assertIn('confidence', result)
            
            if file_type in ('pdf', 'image'):
                self.assertIn('text', result)
            else:
                expected_type = FILE_TYPE_MAPPINGS.get(f'.{file_type}', 'Unknown')
                self.assertEqual(result['type'], expected_type)

if __name__ == '__main__':
    unittest.main()
