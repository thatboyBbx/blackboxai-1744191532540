import os
import logging
from doc_classifier.document_processor import DocumentProcessor
from doc_classifier.gui import Application

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='doc_classifier.log'
    )
    
    # Initialize document processor
    processor = DocumentProcessor()
    
    # Create and run GUI
    app = Application(processor)
    app.mainloop()

if __name__ == '__main__':
    main()
