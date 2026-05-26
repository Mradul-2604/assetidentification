import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.api.schemas import PredictionResponse, ModelPrediction
from app.services.prediction_pipeline import process_image_pipeline

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
async def predict_model(file: UploadFile = File(...)):
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
        return prediction_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")
