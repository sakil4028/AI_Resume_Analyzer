import pdfplumber
from docx import Document


def extract_text_from_pdf(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text


def extract_text_from_docx(docx_path):

    doc = Document(docx_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_text_from_resume(file_path):

    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)

    else:
        return "Unsupported File Format"