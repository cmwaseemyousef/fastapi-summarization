from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# ✅ Load Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ✅ Request Models
class QueryRequest(BaseModel):
    query: str

class SummarizeRequest(BaseModel):
    text: str

# ✅ Root Endpoint
@app.get("/")
def root():
    return {"message": "FastAPI Summarization Service is running!"}

# ✅ Query Processing Endpoint (Fix for 404 error)
@app.post("/query")
def process_query(request: QueryRequest):
    return {"response": f"You sent: {request.query}"}

# ✅ Text Summarization Endpoint
@app.post("/summarize")
def summarize_text(request: SummarizeRequest):
    if len(request.text) < 20:
        raise HTTPException(status_code=400, detail="Text too short for summarization.")
    
    summary = summarizer(request.text, max_length=150, min_length=30, do_sample=False)
    return {"summary": summary[0]["summary_text"]}
