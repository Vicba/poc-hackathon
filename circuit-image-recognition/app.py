import tensorflow as tf
from PIL import Image
import numpy as np
from fastapi import FastAPI
import base64
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import pydantic
import os
from PIL import ImageOps

app = FastAPI()

# Add CORS middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"]
)

# Load the model
model = tf.keras.models.load_model('models/f1-model.h5')

class_mapping = {}
for i, folder in enumerate(os.listdir('data/train_data')):
	class_mapping[i] = folder

class PredictionRequest(pydantic.BaseModel):
	image: str
	label: str

@app.post("/predict")
async def predict(request: PredictionRequest) -> dict:
	# Save the image locally
	with open("image.png", "wb") as f:
		f.write(base64.b64decode(request.image))

	# Preprocess the image
	processed_image = preprocess("image.png")

	# Make prediction using the model
	prediction = model.predict(processed_image)

	# Get the predicted label
	predicted_label_index = np.argmax(prediction)
	predicted_label_text = class_mapping[predicted_label_index]

	print(f"Predicted label: {predicted_label_text}")
	print(f"Actual label: {request.label}")

	# Compare the predicted label text with the provided label text
	return {
		"prediction": predicted_label_text == request.label,
		"predicted_label": predicted_label_text,
	}

def preprocess(image_path: str) -> np.ndarray:
	img = Image.open(image_path)

	# Convert image to RGB mode if it's in RGBA mode
	if img.mode == 'RGBA':
		img = img.convert('RGB')

	# Invert the colors (white to black and vice versa)
	img = ImageOps.invert(img)

	img = img.resize((100, 100))
	img_array = np.array(img) / 255.0
	img_array = np.expand_dims(img_array, axis=0)

	return img_array

if __name__ == '__main__':
	uvicorn.run('app:app', host='localhost', port=8000, reload=True)
