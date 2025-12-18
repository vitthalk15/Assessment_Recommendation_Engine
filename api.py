
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.engine import RecommendationEngine
import uvicorn
import os

app = FastAPI(title="SHL Assessment Recommender", version="1.0")

# Initialize Engine (Lazy loading or startup event)
engine = None

@app.on_event("startup")
def load_model():
    global engine
    print("Initializing Recommendation Engine...")
    engine = RecommendationEngine()
    print("Engine Ready.")

class QueryRequest(BaseModel):
    query: str

class Recommendation(BaseModel):
    Assessment_Name: str
    Assessment_url: str
    Description: str
    Score: float

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

@app.post("/recommend", response_model=list[Recommendation])
def get_recommendations(request: QueryRequest):
    """
    Returns top specific assessment recommendations.
    """
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    try:
        results = engine.search(request.query, top_k=10)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
