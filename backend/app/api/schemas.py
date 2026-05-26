from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ModelPrediction(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_number: str
    model_name: str
    confidence: float
    reasoning: str
    source: str
    image_url: Optional[str] = None
    product_url: Optional[str] = None

class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    asset_name: str
    brand: str
    possible_models: List[ModelPrediction]
    final_prediction: str
    note: str
