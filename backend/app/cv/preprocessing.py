import os
import uuid
from PIL import Image

def preprocess_image(image_path: str) -> str:
    """
    Preprocess image for Gemini Vision API.
    Resizes large images to reduce payload size and ensures RGB format.
    Returns the path to the temporary optimized image.
    """
    try:
        img = Image.open(image_path)
        
        # Convert to RGB (removes alpha channel if PNG, etc.)
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        # Resize if dimensions are too large (e.g., max 1500px on longest side)
        max_dim = 1500
        width, height = img.size
        
        if max(width, height) > max_dim:
            scale = max_dim / max(width, height)
            new_size = (int(width * scale), int(height * scale))
            # LANCZOS is standard high-quality downsampling in modern Pillow
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        # Save to temp directory
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        out_filename = f"{uuid.uuid4().hex}_gemini.jpg"
        out_path = os.path.join(temp_dir, out_filename)
        
        # Save with quality compression suitable for Gemini
        img.save(out_path, "JPEG", quality=85)
        
        return out_path
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        # If Pillow fails, just return original path as fallback
        return image_path
