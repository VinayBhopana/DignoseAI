import os
from io import BytesIO
from PIL import Image
import numpy as np
import json
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.pneumonia.model import PneumoniaModel
from app.pneumonia.schemas import PneumoniaPredictionResponse

def run_prediction(image_path: str):
    # Load the model
    model = PneumoniaModel()

    # Load and preprocess the image
    try:
        with open(image_path, "rb") as f:
            contents = f.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
    except FileNotFoundError:
        print(json.dumps({"detail": f"Image file not found at {image_path}"}))
        return
    except Exception as e:
        print(json.dumps({"detail": f"Invalid image file: {e}"}))
        return

    image = image.resize((150, 150))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, 0)

    # Make prediction
    prob = float(model.predict(img_array))
    diagnosis = "Pneumonia likely" if prob > 0.5 else "Likely normal"

    response = PneumoniaPredictionResponse(pneumonia_probability=prob, diagnosis=diagnosis)
    print(json.dumps(response.model_dump()))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_pneumonia_prediction.py <path_to_image>")
        sys.exit(1)
    
    image_file_path = sys.argv[1]
    run_prediction(image_file_path)

