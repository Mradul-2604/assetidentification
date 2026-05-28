import os
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from PIL import Image
from google import genai
from google.genai import types

class GeminiModelPrediction(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_number: str = Field(description="The exact alphanumeric model number if visible or highly probable")
    model_name: str = Field(description="The full human-readable model name (e.g. 'Samsung Galaxy S23 Ultra')")
    confidence: str = Field(description="Confidence level (e.g. 'High', 'Medium', 'Low') or percentage")
    reasoning: str = Field(description="Brief explanation of why this model was chosen based on visual and textual features")

class GeminiAssetResponse(BaseModel):
    asset_category: str = Field(description="General category (e.g., 'mobile phone', 'refrigerator', 'microwave')")
    brand: str = Field(description="Detected or inferred brand name (e.g. 'Apple', 'Samsung', 'Nothing')")
    visible_text: List[str] = Field(description="Any readable text, labels, or serial numbers found on the device")
    possible_models: List[GeminiModelPrediction] = Field(description="List of top 3 most likely models based on appearance and text")

class GeminiEngine:
    def __init__(self):
        # We rely on the environment variable GEMINI_API_KEY being set
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY environment variable is not set. Gemini API will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
            
    def identify_asset(self, image_path: str) -> GeminiAssetResponse | dict:
        """
        Sends the image to Gemini 2.0 Flash to identify the asset, brand, text, and model.
        """
        if not self.client:
            return {
                "asset_category": "Unknown",
                "brand": "Unknown",
                "visible_text": [],
                "possible_models": []
            }
            
        prompt = """
        You are an expert industrial designer, asset identification specialist, and OCR engine.
        Analyze this image of a product or appliance and return a structured JSON response.
        
        1. Identify the broad asset_category (e.g., 'mobile phone', 'refrigerator', 'microwave', 'coffee machine').
        2. Identify the brand. If explicit text exists, use it. If not, infer from design signatures (e.g. a transparent phone with glyphs is a 'Nothing' phone).
        3. Extract any visible_text, especially model numbers, serial codes, or labels.
        4. Predict the top 1 to 3 possible_models. Provide the full model_name, a clean model_number, your confidence level, and your reasoning. 
           Your reasoning MUST explain what visual design features (camera layout, colors, transparent back, interface) or text led to this conclusion.
           If you cannot clearly read the model number from the image and are guessing based on general shape, you MUST set confidence to 'Low' or a percentage below 50%.
        """
        
        try:
            # Load image using PIL
            img = Image.open(image_path)
            
            response = self.client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "asset_category": {
                                "type": "STRING",
                                "description": "General category (e.g., 'mobile phone', 'refrigerator', 'microwave')"
                            },
                            "brand": {
                                "type": "STRING",
                                "description": "Detected or inferred brand name (e.g. 'Apple', 'Samsung', 'Nothing')"
                            },
                            "visible_text": {
                                "type": "ARRAY",
                                "description": "Any readable text, labels, or serial numbers found on the device",
                                "items": {
                                    "type": "STRING"
                                }
                            },
                            "possible_models": {
                                "type": "ARRAY",
                                "description": "List of top 3 most likely models based on appearance and text",
                                "items": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "model_number": {
                                            "type": "STRING",
                                            "description": "The exact alphanumeric model number if visible or highly probable"
                                        },
                                        "model_name": {
                                            "type": "STRING",
                                            "description": "The full human-readable model name (e.g. 'Samsung Galaxy S23 Ultra')"
                                        },
                                        "confidence": {
                                            "type": "STRING",
                                            "description": "Confidence level (e.g. 'High', 'Medium', 'Low') or percentage"
                                        },
                                        "reasoning": {
                                            "type": "STRING",
                                            "description": "Brief explanation of why this model was chosen based on visual and textual features"
                                        }
                                    },
                                    "required": ["model_number", "model_name", "confidence", "reasoning"]
                                }
                            }
                        },
                        "required": ["asset_category", "brand", "visible_text", "possible_models"]
                    },
                    temperature=0.2, # Low temperature for more deterministic/factual output
                ),
            )
            
            # Response parsed automatically into Pydantic model by the SDK?
            # Actually, google-genai structured output returns a string or object.
            # We can use parsed if available, or parse the JSON string.
            if response.parsed:
                return response.parsed
                
            # Fallback if parsed isn't populated automatically
            import json
            data = json.loads(response.text)
            return GeminiAssetResponse(**data)
            
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return {
                "asset_category": "Unknown",
                "brand": "Unknown",
                "visible_text": [],
                "possible_models": []
            }

gemini_engine = GeminiEngine()
