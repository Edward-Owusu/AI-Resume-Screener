# job_parser.py

from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception as e:
        text = f"[ERROR] Could not read PDF: {e}"
    return text

def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"[ERROR] Could not read DOCX: {e}"
    return text

def extract_text_from_txt(txt_path):
    text = ""
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        text = f"[ERROR] Could not read TXT file: {e}"
    return text
