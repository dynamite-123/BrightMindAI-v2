from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
from ..utils import extract_pdf_to_txt

router = APIRouter(
    prefix='/pdf',
    tags=['pdf']
)

# Create directories for storing files
UPLOAD_DIR = Path("uploads/pdfs")
OUTPUT_DIR = Path("uploads/extracted_texts")

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/extract-text")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and extract text from it
    
    Args:
        file: PDF file to upload and process
    
    Returns:
        JSON response with success status and details
    """
    # Validate file type
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a PDF"
        )
    
    # Generate unique ID for both files
    file_id = str(uuid.uuid4())
    pdf_filename = f"{file_id}.pdf"
    txt_filename = f"{file_id}.txt"
    
    # Define file paths
    pdf_path = UPLOAD_DIR / pdf_filename
    txt_path = OUTPUT_DIR / txt_filename
    
    try:
        # Save uploaded PDF file temporarily
        with open(pdf_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text from PDF
        success = extract_pdf_to_txt(str(pdf_path), str(txt_path))
        
        if success:
            # Get file sizes for response
            pdf_size = os.path.getsize(pdf_path)
            txt_size = os.path.getsize(txt_path) if os.path.exists(txt_path) else 0
            
            response_data = {
                "success": True,
                "message": "Text extracted successfully",
                "details": {
                    "original_filename": file.filename,
                    "pdf_size_bytes": pdf_size,
                    "extracted_text_size_bytes": txt_size,
                    "pdf_id": file_id
                }
            }
            
            # Optional: Clean up the temporary PDF file
            # os.remove(pdf_path)  # Uncomment if you don't want to keep PDFs
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response_data
            )
        else:
            # Clean up files on failure
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            if os.path.exists(txt_path):
                os.remove(txt_path)
                
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to extract text from PDF"
            )
    
    except Exception as e:
        # Clean up files on error
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        if os.path.exists(txt_path):
            os.remove(txt_path)
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for PDF service"""
    return {"status": "healthy", "service": "pdf-extraction"}