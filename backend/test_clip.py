import os
import torch
from app.cv.clip_classifier import clip_classifier
from PIL import Image

uploads_dir = "uploads"
images = [f for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

for img_name in images:
    path = os.path.join(uploads_dir, img_name)
    print(f"\n--- Testing image: {path} ---")
    
    # Let's inspect the probabilities
    image = Image.open(path).convert("RGB")
    categories = clip_classifier.categories
    labels = [f"a photo of a {cat}" for cat in categories]
    
    inputs = clip_classifier.processor(text=labels, images=image, return_tensors="pt", padding=True).to(clip_classifier.device)
    
    with torch.no_grad():
        outputs = clip_classifier.model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)[0].cpu().numpy()
        
    for cat, prob in zip(categories, probs):
        print(f"{cat}: {prob:.4f}")
    
    pred = clip_classifier.identify_asset(path)
    print(f"Final Prediction: {pred}")
