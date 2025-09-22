import tensorflow as tf
from tensorflow.keras.models import load_model
import os

class PneumoniaModel:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "models", "pneumonia_model.h5")
        self.model = load_model(model_path)

    def predict(self, img_tensor):

        prediction = self.model.predict(img_tensor)  # prediction shape might be (1,1) or (1,2)

        if prediction.shape[1] == 1:
            # sigmoid output (single probability)
            pneumonia_prob = prediction[0][0]
        else:
            # softmax output (two class probabilities)
            pneumonia_prob = prediction[0][1]

        return pneumonia_prob

