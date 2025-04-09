import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable
from doc_classifier.document_processor import DocumentProcessor
import logging
import os

class Application(tk.Tk):
    def __init__(self, processor: DocumentProcessor):
        super().__init__()
        self.processor = processor
        self.title("Zimbabwe Ministry of ICT - Document Classifier")
        self.geometry("800x600")
        self.create_widgets()
        self.logger = logging.getLogger(__name__)
        
    def create_widgets(self):
        """Create all GUI components"""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Document Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_entry = ttk.Entry(file_frame)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(
            file_frame, 
            text="Browse...", 
            command=self.browse_file
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Process button
        process_btn = ttk.Button(
            main_frame,
            text="Process Document",
            command=self.process_document
        )
        process_btn.pack(pady=10)
        
        # Results display
        results_frame = ttk.LabelFrame(main_frame, text="Classification Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(
            results_frame,
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def browse_file(self):
        """Open file dialog to select document"""
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("All Supported Files", "*.pdf;*.png;*.jpg;*.jpeg;*.docx;*.xlsx;*.pptx"),
                ("PDF Files", "*.pdf"),
                ("Image Files", "*.png;*.jpg;*.jpeg"),
                ("Word Documents", "*.docx"),
                ("Excel Files", "*.xlsx"),
                ("PowerPoint Files", "*.pptx")
            ]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            
    def process_document(self):
        """Process the selected document"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a document first")
            return
            
        try:
            self.status_var.set("Processing...")
            self.update()
            
            result = self.processor.process_file(file_path)
            self.display_results(result)
            self.status_var.set("Document processed successfully")
            
        except Exception as e:
            self.logger.error(f"Error processing document: {str(e)}")
            messagebox.showerror(
                "Processing Error",
                f"An error occurred while processing the document:\n{str(e)}"
            )
            self.status_var.set("Error processing document")
            
    def display_results(self, result: dict):
        """Display classification results in the text widget"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        text = f"File: {os.path.basename(result['file_path'])}\n"
        text += f"Type: {result['type']}\n"
        text += f"Confidence: {result['confidence']:.2%}\n\n"
        text += "Extracted Text:\n"
        text += result['text']
        
        self.results_text.insert(tk.END, text)
        self.results_text.config(state=tk.DISABLED)
        
    def run(self):
        """Run the application"""
        self.mainloop()
