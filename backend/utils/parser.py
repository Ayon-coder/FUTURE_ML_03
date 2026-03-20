import io
from pypdf import PdfReader

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    text = ""
    try:
        if filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        else:
            text = file_content.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
    
    return text
