
from PyPDF2 import PdfReader


def extract_resume_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = []

    for page in reader.pages:
        text.append(page.extract_text() or "")

    return "\n".join(text)