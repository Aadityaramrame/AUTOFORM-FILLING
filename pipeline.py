import pytesseract
from pdf2image import convert_from_path
import google.generativeai as genai
import os, json

# --- Form Schema ---
FORMS = {
    "pancard_form": [
        "Name", "DOB", "Gender", "FatherName", "MotherName",
        "Address", "City", "State", "Pincode", "Mobile", "Email",
        "DocumentType", "DocumentNumber", "IssueAuthority",
        "IssueDate", "ExpiryDate"
    ]
}

# --- Configure Gemini ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Please set it in Hugging Face Space Secrets.")
genai.configure(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page) + "\n"
    return text.strip()

def extract_key_values_with_gemini(raw_text, form_type="pancard_form"):
    prompt = f"""
You are an intelligent document parser.
Given the following document text, extract only these fields: {FORMS[form_type]}.
Return strictly as JSON key-value pairs.
Document text:
{raw_text}
"""
    
    # Use the supported model
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    print("Gemini API called successfully ✅")
    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except Exception:
        return {"raw_output": response.text}
