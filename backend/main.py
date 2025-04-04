from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import tempfile
import tensorflow as tf
import uvicorn
import os
import logging
from azure.storage.blob import BlobServiceClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app setup
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://alethia2104.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Blob Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=nexus2104;AccountKey=k7MqNBsl8a52tXTFUmwtQCgQfbovbZfFsW4nb1OnTXbjO1ybnBONmFJprz58ZosxJ73gMG/M8op2+AStTuHuMA==;EndpointSuffix=core.windows.net"

CONTAINER_NAME = "models"
BLOB_NAME = "model.keras"

def download_model_from_azure():
    """Downloads the model file from Azure Blob Storage to a temporary file."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".keras") as temp_model_file:
            logger.info(f"Downloading model from Azure Storage: {BLOB_NAME}")
            model_data = blob_client.download_blob()
            temp_model_file.write(model_data.readall())  # Ensure full file is read
            temp_model_path = temp_model_file.name

        logger.info("Model downloaded successfully from Azure.")
        return temp_model_path

    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise

# Load the deepfake detection model from Azure
model_path = download_model_from_azure()
model = tf.keras.models.load_model(model_path)
logger.info("MODEL loaded Successfully")

# Constants
FRAME_COUNT = 10
FRAME_SIZE = (128, 128)

def preprocess_video(video_path):
    """Extracts and preprocesses frames from a video file."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames < FRAME_COUNT:
        return None

    frame_indices = np.linspace(0, total_frames - 1, FRAME_COUNT, dtype=int)

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, FRAME_SIZE)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame / 255.0
        frames.append(frame)

    cap.release()

    if len(frames) != FRAME_COUNT:
        return None

    return np.expand_dims(np.array(frames), axis=0)

@app.post("/detect/")
async def detect_deepfake_video(file: UploadFile = File(...)):
    """Detect deepfake videos using the loaded AI model."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(await file.read())
            video_path = temp_file.name

        video_frames = preprocess_video(video_path)
        if video_frames is None:
            return {"error": "Not enough frames extracted or video processing failed."}

        prediction = model.predict(video_frames)[0]
        real_score, deepfake_score = prediction

        os.unlink(video_path)  # Clean up temp file

        return {
            "deepfake": bool(deepfake_score > real_score),
            "scores": {"real": float(real_score), "deepfake": float(deepfake_score)},
        }
    except Exception as e:
        logger.error(f"Error in detection: {e}")
        return {"error": f"Internal Server Error: {str(e)}"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  
    uvicorn.run(app, host="0.0.0.0", port=port)