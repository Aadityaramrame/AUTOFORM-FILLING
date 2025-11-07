from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import tempfile
from pipeline import extract_text_from_pdf, extract_key_values_with_gemini

app = FastAPI(title="AutoFill Form Extractor API")

FIELDS = [
    "Name", "DOB", "Gender", "FatherName", "MotherName",
    "Address", "City", "State", "Pincode", "Mobile", "Email",
    "DocumentType", "DocumentNumber", "IssueAuthority",
    "IssueDate", "ExpiryDate"
]

@app.post("/extract")
async def extract_api(file: UploadFile):
    if not file:
        return JSONResponse(content={"success": False, "error": "No file uploaded."})
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        result = extract_key_values_with_gemini(text, FIELDS)
        return JSONResponse(content={"success": True, "data": result})

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})

@app.get("/")
def home():
    return {"message": "AutoFill Form API is running!"}
