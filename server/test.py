import os
from app.utils import extract_pdf_to_txt

if __name__ == "__main__":
    # Replace with your PDF path
    pdf_path = "/mnt/c/Users/Anirudh Kashyap/Desktop/test/big.pdf"
    txt_path = "/mnt/c/Users/Anirudh Kashyap/Desktop/test/big.txt"
    
    print("🚀 Testing PDF extraction...")
    print(f"PDF: {pdf_path}")
    print(f"Output: {txt_path}")
    
    try:
        success = extract_pdf_to_txt(pdf_path, txt_path)
        
        if success and os.path.exists(txt_path):
            file_size = os.path.getsize(txt_path)
            print(f"✅ SUCCESS - Text extracted ({file_size} bytes)")
            
            # Show first 200 characters
            with open(txt_path, 'r', encoding='utf-8') as f:
                preview = f.read(200)
                print(f"Preview: {preview}{'...' if len(preview) >= 200 else ''}")
        else:
            print("❌ FAILED - Extraction unsuccessful")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")