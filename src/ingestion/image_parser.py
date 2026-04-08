import os

def extract_image_chunks(doc, pdf_path: str):
    """
    Extract image chunks from PDF document
    """
    image_chunks = []
    source = os.path.basename(pdf_path)

    for page_number, page in enumerate(doc, start=1):
        images = page.get_images(full=True)
        for idx, _ in enumerate(images):
            image_chunks.append({
                "content": f"Image {idx + 1} from page {page_number}",
                "type": "image",
                "page": page_number,
                "source": source
            })

    return image_chunks