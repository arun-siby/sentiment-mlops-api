import os
import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from transformers import pipeline
from prometheus_client import make_asgi_app, Counter, Histogram
import uvicorn

# Initialize the API
app = FastAPI(title="Sentiment Analysis API")

# --- PROMETHEUS METRICS ---
# Track how many requests we get
REQUEST_COUNT = Counter(
    "sentiment_api_requests_total", 
    "Total number of requests", 
    ["endpoint", "method"]
)
# Track how long requests take
REQUEST_LATENCY = Histogram(
    "sentiment_api_latency_seconds", 
    "Request latency in seconds", 
    ["endpoint"]
)
# Track what the AI predicts (Positive vs Negative)
PREDICTION_COUNT = Counter(
    "model_predictions_total", 
    "Sentiment predictions made", 
    ["sentiment"]
)

# Enable the /metrics endpoint so Prometheus can read our data
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# --- AI MODEL SETUP ---
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_pipeline = None

@app.on_event("startup")
async def load_model():
    """Load the AI model when the server starts."""
    global sentiment_pipeline
    print(f"Loading model: {model_name}...")
    sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)
    print("Model loaded successfully!")

# --- DATA FORMAT ---
class SentimentRequest(BaseModel):
    text: str

# --- MIDDLEWARE (The Timer) ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Record stats for Prometheus
    REQUEST_COUNT.labels(endpoint=request.url.path, method=request.method).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
    
    return response

# --- ENDPOINTS ---
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "MLOps API is running!"}

@app.post("/predict")
def predict(request: SentimentRequest):
    if not sentiment_pipeline:
        raise HTTPException(status_code=503, detail="Model is still loading...")
    
    # Run the AI
    result = sentiment_pipeline(request.text)[0]
    
    # Log the result to Prometheus
    PREDICTION_COUNT.labels(sentiment=result['label']).inc()
    
    return {
        "text": request.text,
        "sentiment": result['label'],
        "confidence": result['score']
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)