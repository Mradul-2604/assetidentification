import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

import torch
from app.cv.clip_classifier import clip_classifier
from PIL import Image

uploads_dir = "uploads"
images = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

prompt_ensembles = {
    "mobile phone": [
        "a photo of a mobile phone",
        "a smartphone",
        "a cell phone",
        "a phone"
    ],
    "microwave": [
        "a photo of a microwave oven",
        "a microwave kitchen appliance",
        "a microwave"
    ],
    "refrigerator": [
        "a photo of a refrigerator",
        "a kitchen fridge",
        "a double door refrigerator",
        "a silver refrigerator"
    ],
    "water dispenser": [
        "a photo of a water dispenser",
        "a water cooler dispenser",
        "a bottled water dispenser"
    ],
    "holding cabinet": [
        "a food holding cabinet",
        "a warming holding cabinet",
        "a commercial hot cabinet"
    ],
    "coffee machine": [
        "a photo of a coffee machine",
        "a coffee maker",
        "an espresso machine"
    ],
    "ice machine": [
        "an ice maker machine",
        "a commercial ice machine",
        "an ice dispenser"
    ],
    "oven": [
        "a photo of a kitchen oven",
        "a baking oven appliance",
        "a wall oven"
    ]
}

for img_name in images:
    path = os.path.join(uploads_dir, img_name)
    print(f"\n--- Testing image: {path} ---")
    
    image = Image.open(path).convert("RGB")
    
    # Let's test standard classification first
    pred = clip_classifier.identify_asset(path)
    print(f"Standard Prediction: {pred}")
    
    # Let's test prompt ensembled classification
    # Calculate scores for each category
    category_scores = {}
    
    for category, prompts in prompt_ensembles.items():
        inputs = clip_classifier.processor(text=prompts, images=image, return_tensors="pt", padding=True).to(clip_classifier.device)
        with torch.no_grad():
            outputs = clip_classifier.model(**inputs)
            logits_per_image = outputs.logits_per_image
            # Average logit score for these prompts
            avg_score = logits_per_image.mean().item()
            category_scores[category] = avg_score
            
    # Sort categories by average score
    sorted_cats = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    print("Ensemble Scores:")
    for cat, score in sorted_cats:
        print(f"  {cat}: {score:.4f}")
        
    print(f"Ensemble Prediction: {sorted_cats[0][0]}")
