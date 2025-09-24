from passlib.context import CryptContext
import fitz  # PyMuPDF

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hashing and security
def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def extract_pdf_to_txt(pdf_path: str, txt_path: str) -> bool:
    """
    Extract text from PDF and save to txt file
    
    Args:
        pdf_path (str): Path to the input PDF file
        txt_path (str): Path to save the extracted text
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            with fitz.open(pdf_path) as pdf_doc:
                for page_num in range(len(pdf_doc)):
                    page = pdf_doc.load_page(page_num)
                    text = page.get_text()
                    txt_file.write(text)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
