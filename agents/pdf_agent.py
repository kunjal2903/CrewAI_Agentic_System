import fitz
from utils.pdf_utils import extract_text_from_pdf
from utils.embedding_utils import generate_embedding, store_embedding

def process_pdf(file):
    pdf_content = extract_text_from_pdf(file)
    embedding = generate_embedding(pdf_content)
    store_embedding(file.filename, embedding)
    return {"message": "PDF processed and embedded successfully"}
