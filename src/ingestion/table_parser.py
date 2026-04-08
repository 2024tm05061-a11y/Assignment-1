import os
from unstructured.partition.pdf import partition_pdf

def extract_table_chunks(pdf_path: str):
    """
    Extract table chunks from PDF
    """
    elements = partition_pdf(pdf_path)
    table_chunks = []
    source = os.path.basename(pdf_path)

    for element in elements:
        if element.category == "Table":
            table_chunks.append({
                "content": str(element),
                "type": "table",
                "page": element.metadata.page_number,
                "source": source
            })

    return table_chunks