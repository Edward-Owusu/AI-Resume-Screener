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
    # Ensure the text is safely encoded for Streamlit
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"[ERROR] Could not read DOCX: {e}"
    # Ensure the text is safely encoded for Streamlit
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
