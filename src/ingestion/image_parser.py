import os
import fitz  # PyMuPDF
from PIL import Image


def extract_images(doc, pdf_path: str, output_dir="data/images"):
    """
    Extract images from PDF pages and save them to disk
    """
    os.makedirs(output_dir, exist_ok=True)

    image_metadata = []

    for page_number, page in enumerate(doc, start=1):
        images = page.get_images(full=True)

        for idx, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_name = f"page_{page_number}_img_{idx + 1}.png"
            image_path = os.path.join(output_dir, image_name)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            image_metadata.append({
                "image_path": image_path,
                "page": page_number,
                "source": os.path.basename(pdf_path)
            })

    return image_metadata