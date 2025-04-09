from setuptools import setup, find_packages

setup(
    name='doc_classifier',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytesseract',
        'opencv-python',
        'pandas',
        'scikit-learn',
        'nltk',
        'python-docx',
        'openpyxl',
        'python-pptx',
        'requests',
        'kaggle',
        'pdf2image'
    ],
    entry_points={
        'console_scripts': [
            'doc-classifier=doc_classifier.main:main',
        ],
    },
)
