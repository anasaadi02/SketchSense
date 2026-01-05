from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model_service import DrawingModel
from typing import Optional

app = FastAPI(
    title="SketchSense API",
    description="AI-powered drawing recognition API",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Alternative React port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model (lazy loading)
drawing_model: Optional[DrawingModel] = None

def get_model():
    """Get or initialize the drawing model"""
    global drawing_model
    if drawing_model is None:
        drawing_model = DrawingModel('models/drawing_model.h5')
    return drawing_model

# Pydantic models for request/response
class ImageRequest(BaseModel):
    image: str  # Base64 encoded image data

class PredictionResponse(BaseModel):
    success: bool
    predictions: list[dict]
    top_guess: Optional[dict] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool

@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {"message": "SketchSense API is running"}

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health():
    """Health check endpoint"""
    model = get_model()
    return {
        "status": "ok",
        "model_loaded": model.model is not None
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: ImageRequest):
    """
    Predict what the drawing is
    
    - **image**: Base64 encoded image data (can include data URL prefix)
    - Returns top 5 predictions with confidence scores
    """
    try:
        model = get_model()
        
        if model.model is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Please check model path."
            )
        
        # Predict
        predictions = model.predict(request.image, top_k=5)
        
        if not predictions:
            raise HTTPException(
                status_code=500,
                detail="No predictions returned"
            )
        
        return {
            "success": True,
            "predictions": predictions,
            "top_guess": predictions[0] if predictions else None
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    print("Starting SketchSense API...")
    try:
        get_model()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load model on startup: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)