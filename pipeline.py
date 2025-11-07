import pytesseract
from pdf2image import convert_from_path
import google.generativeai as genai
import os, json

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Set it in Render Environment Variables.")
genai.configure(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page) + "\n"
    return text.strip()

def extract_key_values_with_gemini(raw_text, fields):
    prompt = f"""
You are an intelligent document parser.
Given the following document text, extract only these fields: {fields}.
Return strictly as JSON key-value pairs.
Document text:
{raw_text}
"""
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Cleanup
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        extracted = json.loads(text)
    except Exception:
        extracted = {"raw_output": text}

    # Ensure all fields exist
    return {field: extracted.get(field, "") for field in fields}
