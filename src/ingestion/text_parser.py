import os

def extract_text_chunks(doc, pdf_path: str):
    """
    Extract text chunks from PDF document
    """
    text_chunks = []
    source = os.path.basename(pdf_path)

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            text_chunks.append({
                "content": text,
                "type": "text",
                "page": page_number,
                "source": source
            })

    return text_chunks