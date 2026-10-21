"""
PDF Parser Module
Extracts text from PDF files
"""
import io
import pdfplumber


def extract_text_from_pdf(pdf_file):
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_file: File object from Streamlit file uploader
        
    Returns:
        str: Extracted text from PDF
        
    Raises:
        Exception: If PDF parsing fails
    """
    text = ""
    
    pdf_file.seek(0)
    pdf_bytes = io.BytesIO(pdf_file.read())
    pdf_file.seek(0)
    
    try:
        with pdfplumber.open(pdf_bytes) as pdf:
            if not pdf.pages:
                raise ValueError("PDF contains no pages")
            
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if text.strip():
            return text.strip()
        
        raise ValueError(
            "No text could be extracted. The PDF may be image-based or contain only images. "
            "Please use a text-based PDF or convert images to text first."
        )
        
    except ValueError:
        raise
    except Exception as e:
        error_msg = str(e).lower()
        if "password" in error_msg or "encrypted" in error_msg:
            raise ValueError("PDF is password-protected. Please provide an unprotected version.")
        raise Exception(f"Error parsing PDF: {str(e)}")
