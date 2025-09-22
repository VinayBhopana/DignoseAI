from pydantic import BaseModel

class PneumoniaPredictionResponse(BaseModel):
    pneumonia_probability: float
    diagnosis: str

    class Config:
        schema_extra = {
            "example": {
                "pneumonia_probability": 0.87,
                "diagnosis": "Pneumonia likely"
            }
        }
