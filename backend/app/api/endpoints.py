import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.schemas import PredictionResponse, ModelPrediction, PredictionHistoryResponse
from app.services.prediction_pipeline import process_image_pipeline
from app.db.database import get_db
from app.db.models import PredictionHistory


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Image uploaded successfully", "filename": file.filename, "file_path": file_path}

@router.post("/predict-model", response_model=PredictionResponse)
async def predict_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Main endpoint that runs the entire prediction pipeline:
    1. Preprocesses image
    2. Identifies asset category (CLIP)
    3. Detects brand and OCR text (EasyOCR)
    4. Retrieves candidate models (Tavily)
    5. Computes similarities (CLIP)
    6. Returns final prediction
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Save the file temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Run the full pipeline
        prediction_result = await process_image_pipeline(file_path)
        
        # Save prediction to history database
        confidence = 0.0
        if prediction_result.possible_models:
            confidence = max((m.confidence for m in prediction_result.possible_models), default=0.0)
            
        history_record = PredictionHistory(
            brand=prediction_result.brand,
            model_name=prediction_result.final_prediction,
            confidence=confidence,
            image_path=f"/uploads/{file.filename}"
        )
        db.add(history_record)
        db.commit()
        db.refresh(history_record)
        
        return prediction_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")

@router.get("/history", response_model=List[PredictionHistoryResponse])
def get_history(brand: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PredictionHistory)
    if brand and brand.strip().lower() != "nothing":
        query = query.filter(PredictionHistory.brand.ilike(f"%{brand}%"))
    
    records = query.order_by(desc(PredictionHistory.timestamp)).all()
    return records
