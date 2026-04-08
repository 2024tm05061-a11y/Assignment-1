import fitz  # PyMuPDF

def load_pdf(pdf_path: str):
    """
    Load PDF and return the PyMuPDF document object
    """
    return fitz.open(pdf_path)
