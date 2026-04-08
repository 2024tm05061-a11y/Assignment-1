from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_parser import extract_text_chunks
from src.ingestion.table_parser import extract_table_chunks
from src.ingestion.image_parser import extract_images
PDF_PATH = "sample_documents/08_OperatingManualETF90.pdf"
import os
import os

CURRENT_FILE_DIR = os.path.dirname(__file__)
INGESTION_DIR = os.path.abspath(CURRENT_FILE_DIR)
SRC_DIR = os.path.abspath(os.path.join(INGESTION_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, ".."))

PDF_PATH = os.path.join(
    PROJECT_ROOT,
    "sample_documents",
    "08_OperatingManualETF90.pdf"
)

print("DEBUG PDF_PATH:", PDF_PATH)
print("DEBUG file exists:", os.path.exists(PDF_PATH))

# Absolute path to project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

PDF_PATH = os.path.join(
    BASE_DIR,
    "sample_documents",
    "08_OperatingManualETF90.pdf"
)
print("PDF_PATH resolved to:", PDF_PATH)
print("PDF exists:", os.path.exists(PDF_PATH))
def get_all_chunks(pdf_path: str):
    doc = load_pdf(pdf_path)

    # text + table
    text_chunks = extract_text_chunks(doc, PDF_PATH)
    table_chunks = extract_table_chunks(PDF_PATH)

    # image handling with VLM
    image_files = extract_images(doc, PDF_PATH)
    image_summary_chunks = []

    for img in image_files:
        caption = generate_image_caption(img["image_path"])
        image_summary_chunks.append({
            "content": caption,
            "type": "image_summary",
            "page": img["page"],
            "source": img["source"]
        })

    return text_chunks + table_chunks + image_summary_chunks
