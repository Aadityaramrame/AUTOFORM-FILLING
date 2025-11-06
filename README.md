Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
# 🧠 AutoFill Form Extractor

This app extracts structured information from documents (like PAN Card forms) using:
- **OCR (pytesseract)** for text extraction
- **Gemini 2.5 Flash** for intelligent field parsing

## 🚀 How to Use
1. Upload a PDF document (e.g., PAN Card)
2. Select the form type
3. View the extracted JSON output

## 🧩 Tech Stack
- Python + Gradio
- Google Gemini API
- Tesseract OCR
- pdf2image
