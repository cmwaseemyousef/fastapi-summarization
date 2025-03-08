import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Download NLTK sentence tokenizer
nltk.download('punkt')

# Add Response Models
class QueryResponse(BaseModel):
    response: str

class SummaryResponse(BaseModel):
    summary: str

# Initialize FastAPI app
app = FastAPI()

# Disable rate limiting for tests
DISABLE_RATE_LIMITING = os.getenv("DISABLE_RATE_LIMITING", "false").lower() == "true"

if not DISABLE_RATE_LIMITING:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ✅ Load Summarization Model
summarizer = pipeline("summarization", model="t5-small")

# ✅ Request Models
class QueryRequest(BaseModel):
    query: str

class SummarizationRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "FastAPI Summarization Service is running!"}

@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    return {"response": f"You sent: {request.query}"}

@app.post("/summarize", response_model=SummaryResponse)
def summarize_text(request: SummarizationRequest):
    if len(request.text) > 10000:
        raise HTTPException(status_code=400, detail="Text too long. Maximum 10000 characters allowed.")
    if len(request.text.split()) < 20:
        raise HTTPException(status_code=400, detail="Text too short for summarization. Please provide at least 20 words.")

    raw_summary = summarizer(
        request.text,
        max_length=50,
        min_length=25,
        length_penalty=2.5,
        num_beams=10,
        early_stopping=True
    )[0]["summary_text"]

    # Apply NLTK Sentence Compression
    sentences = sent_tokenize(raw_summary)
    condensed_summary = " ".join(sentences[:2])  # Keep only the first 2 key sentences

    return {"summary": condensed_summary}