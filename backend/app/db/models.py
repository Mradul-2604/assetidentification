from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model_name = Column(String)
    confidence = Column(Float)
    image_path = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
