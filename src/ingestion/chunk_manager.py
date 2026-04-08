from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_parser import extract_text_chunks
from src.ingestion.image_parser import extract_image_chunks
from src.ingestion.table_parser import extract_table_chunks

PDF_PATH = "sample_documents/08_OperatingManualETF90.pdf"

def get_all_chunks():
    doc = load_pdf(PDF_PATH)

    text_chunks = extract_text_chunks(doc, PDF_PATH)
    image_chunks = extract_image_chunks(doc, PDF_PATH)
    table_chunks = extract_table_chunks(PDF_PATH)

    return text_chunks + table_chunks + image_chunks
