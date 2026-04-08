from src.pdf_loader import load_pdf
from src.text_parser import extract_text_chunks
from src.table_parser import extract_table_chunks
from src.image_parser import extract_images
from src.models.image_captioner import generate_image_caption

PDF_PATH = "sample_documents/08_OperatingManualETF90.pdf"

def get_all_chunks():
    doc = load_pdf(PDF_PATH)

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
