from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# ✅ Load Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ✅ Request Models
class QueryRequest(BaseModel):
    query: str

class SummarizationRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "FastAPI Summarization Service is running!"}

@app.post("/query")
def process_query(request: QueryRequest):
    return {"response": f"You sent: {request.query}"}

@app.post("/summarize")
def summarize_text(request: SummarizationRequest):
    if len(request.text.split()) < 20:
        raise HTTPException(status_code=400, detail="Text too short for summarization. Please provide at least 20 words.")

    summary = summarizer(
        request.text,
        max_length=80,
        min_length=20,
        length_penalty=1.5,
        num_beams=6,
        do_sample=False
    )

    return {"summary": summary[0]["summary_text"]}
