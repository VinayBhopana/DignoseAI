from fastapi import APIRouter, File, UploadFile, HTTPException
from io import BytesIO
from PIL import Image
import numpy as np
from .model import PneumoniaModel
from .schemas import PneumoniaPredictionResponse

router = APIRouter()

model = PneumoniaModel()

@router.post("/predict", response_model=PneumoniaPredictionResponse)
async def pneumonia_predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Use JPEG or PNG.")
    contents = await file.read()
    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except:
        raise HTTPException(status_code=400, detail="Invalid image file.")
    
    image = image.resize((150, 150))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, 0)
    
    prob = float(model.predict(img_array))
    diagnosis = "Pneumonia likely" if prob > 0.5 else "Likely normal"
    
    return PneumoniaPredictionResponse(pneumonia_probability=prob, diagnosis=diagnosis)
