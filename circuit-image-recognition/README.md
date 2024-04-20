# Circuit Image Recognition

This project aims to create an image recognition system for identifying circuit diagrams using machine learning. The system uses a FastAPI web server to provide an API endpoint for making predictions on circuit images.

## Features

- Accepts base64-encoded circuit images as input for prediction
- Utilizes a pre-trained deep learning model for image classification
- Provides a RESTful API endpoint for making predictions
- Supports Docker deployment for easy scalability and portability

## Installation

### Development

Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

Run the FastAPI server using the following command:

```bash
python app.py
```

### Docker

Build the Docker image using the following command:

```bash
docker build -t circuit-image-recognition .
```

## Usage

Access the endpoint at `http://localhost:8000/predict` to make predictions on circuit images. The endpoint accepts a POST request with a JSON payload containing the base64-encoded image data.

```json
{
  "image": "<base64-encoded-image-data>",
  "label": "<circuit-label>"
}
```
