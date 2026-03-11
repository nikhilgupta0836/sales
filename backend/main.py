from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr
import pandas as pd

from ai import generate_summary
from email_service import send_email

app = FastAPI(title="Sales Insight Automator")

# Enable CORS so frontend (localhost:3000) can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), email: EmailStr = Form(...)):

    try:

        # Validate file type
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)

        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)

        else:
            raise HTTPException(status_code=400, detail="Only CSV or XLSX files allowed")

        # Preview dataset
        preview = df.head(20).to_string()

        # Generate AI summary
        summary = generate_summary(preview)

        # Send email (or simulated email)
        send_email(email, summary)

        return {
            "status": "success",
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))