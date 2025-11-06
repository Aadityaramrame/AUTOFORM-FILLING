from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn, os, tempfile
from pipeline import extract_text_from_pdf, extract_key_values_with_gemini

app = FastAPI(title="AutoFill Form Extractor API")

@app.post("/extract")
async def extract_api(file: UploadFile, form_type: str = Form("pancard_form")):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        result = extract_key_values_with_gemini(text, form_type=form_type)

        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})

@app.get("/")
def home():
    return {"message": "AutoFill Form API is running! Use POST /extract with a PDF."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
