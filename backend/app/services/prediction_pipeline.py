from app.cv.preprocessing import preprocess_image
from app.ai.gemini_engine import gemini_engine
from app.scraper.tavily_search import tavily_searcher
from app.api.schemas import PredictionResponse, ModelPrediction

async def process_image_pipeline(image_path: str) -> PredictionResponse:
    # 1. Preprocess Image (Resize and compress via Pillow)
    optimized_image_path = preprocess_image(image_path)
    
    # 2. Gemini Multimodal Reasoning
    gemini_result = gemini_engine.identify_asset(optimized_image_path)
    
    # Check if we got a fallback dict or the pydantic model
    if isinstance(gemini_result, dict):
        asset_category = gemini_result.get("asset_category", "Unknown")
        brand = gemini_result.get("brand", "Unknown")
        gemini_models = gemini_result.get("possible_models", [])
        visible_text = gemini_result.get("visible_text", [])
    else:
        asset_category = gemini_result.asset_category
        brand = gemini_result.brand
        gemini_models = gemini_result.possible_models
        visible_text = gemini_result.visible_text
        
    final_models = []
    
    # 3. External Validation via Tavily
    for m in gemini_models:
        model_name = m.get("model_name", "") if isinstance(m, dict) else m.model_name
        model_number = m.get("model_number", "") if isinstance(m, dict) else m.model_number
        confidence = m.get("confidence", "Low") if isinstance(m, dict) else m.confidence
        reasoning = m.get("reasoning", "") if isinstance(m, dict) else m.reasoning
        
        # Ask Tavily to fetch an official product image and trusted source URL
        tavily_data = tavily_searcher.fetch_model_validation(model_name, asset_category)
        
        # Calculate Deterministic Confidence Score
        score = 0.0
        
        # 1. Gemini Base Certainty
        gemini_conf = str(confidence).lower()
        if "high" in gemini_conf:
            score += 30.0
        elif "medium" in gemini_conf:
            score += 15.0
        elif "low" in gemini_conf:
            score += 5.0
        else:
            import re
            match = re.search(r'(\d+)', gemini_conf)
            if match:
                score += min(float(match.group(1)), 100.0) * 0.3
            else:
                score += 10.0
                
        # 2. Text/OCR Match
        text_matched = False
        for text in visible_text:
            if model_number.lower() in text.lower() and model_number != "Unknown" and model_number.strip():
                text_matched = True
                break
        if text_matched:
            score += 25.0
        elif any(word.lower() in [t.lower() for t in visible_text] for word in model_name.split() if len(word) > 3):
            score += 10.0
            
        # 3. Brand Match
        if brand.lower() != "unknown" and brand.lower() in model_name.lower():
            score += 15.0
            
        # 4. Tavily Validation
        source_url = tavily_data.get("source", "")
        if source_url and source_url not in ["API Key Missing", "Search Failed", "Local Fallback"]:
            score += 10.0
            trusted = ["samsung.com", "apple.com", "gsmarena.com", "amazon", "bestbuy"]
            if any(d in source_url.lower() for d in trusted):
                score += 10.0
        if tavily_data.get("image_url"):
            score += 5.0
            
        # 5. Asset Category Match
        if asset_category.lower() != "unknown" and asset_category.lower() in model_name.lower():
            score += 5.0
            
        # Clamp confidence to max 95.0 and minimum 0.0, save as ratio (0.0 to 0.95)
        # If score is 0 due to some edge case, default to 0.50.
        if score <= 0.0:
            score = 50.0
        score = max(0.0, min(score, 95.0))
        final_confidence = score / 100.0
        
        final_models.append(ModelPrediction(
            model_number=model_number,
            model_name=model_name,
            confidence=final_confidence,
            reasoning=reasoning,
            source=source_url or "Gemini Inference",
            image_url=tavily_data.get("image_url", None)
        ))
        
    # Determine final prediction
    final_pred_name = final_models[0].model_name if final_models else f"{brand} {asset_category}".strip()
    
    # Fallback if Gemini returns absolutely nothing
    if not final_models:
        fallback_model = ModelPrediction(
            model_number="Unknown",
            model_name=f"{brand} {asset_category}".strip(),
            confidence=0.50,
            reasoning="Gemini failed to identify specific models.",
            source="Local Fallback",
            image_url=None
        )
        final_models.append(fallback_model)
        final_pred_name = fallback_model.model_name
        
    note = f"Identified via Gemini 2.0 Flash. Extracted text: {', '.join(visible_text) if visible_text else 'None'}."
        
    return PredictionResponse(
        asset_name=f"{brand} {asset_category}".strip() if brand != "Unknown" else asset_category.capitalize(),
        brand=brand,
        possible_models=final_models,
        final_prediction=final_pred_name,
        note=note
    )
