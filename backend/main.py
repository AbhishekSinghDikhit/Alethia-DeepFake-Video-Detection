from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import tempfile
import tensorflow as tf
import uvicorn
import os
from google.cloud import storage
from google.auth.exceptions import RefreshError
from dotenv import load_dotenv
import base64
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://alethia2104.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load GCP credentials
gcp_b64 = os.getenv("GCP_SERVICE_ACCOUNT_KEY_B64")
if gcp_b64:
    try:
        logger.info("Decoding GCP service account key...")
        gcp_json = json.loads(base64.b64decode(gcp_b64).decode())
        gcp_key_path = os.path.join(tempfile.gettempdir(), "gcp-key.json")  # Use temp dir for portability
        os.makedirs(os.path.dirname(gcp_key_path), exist_ok=True)
        with open(gcp_key_path, "w") as f:
            json.dump(gcp_json, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key_path
        logger.info(f"GCP key written to: {gcp_key_path}")
    except Exception as e:
        logger.error(f"Failed to decode and save GCP key: {e}")
        raise RuntimeError(f"Failed to decode and save GCP key: {e}")
else:
    raise ValueError("GCP service account key not found in environment variables")

# Initialize GCS client with error handling
try:
    client = storage.Client()
    logger.info("GCS client initialized successfully")
except RefreshError as e:
    logger.error(f"GCS authentication failed: {e}")
    raise RuntimeError(f"GCS authentication failed: {e}")
except Exception as e:
    logger.error(f"Failed to initialize GCS client: {e}")
    raise RuntimeError(f"Failed to initialize GCS client: {e}")

# client = storage.Client()

# def download_model():
#     client = storage.Client()
#     bucket = client.bucket("alethia_model")
#     blob = bucket.blob("deepfake_detection_model.keras")
#     os.makedirs("models", exist_ok=True)  # Ensure the folder exists
#     blob.download_to_filename("models/deepfake_detection_model.keras")

# # Call this before loading the model
# download_model()
# model = tf.keras.models.load_model("models/deepfake_detection_model.keras")

# # Load the deepfake detection model
# base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
# model_path = os.path.join(base_dir, "models", "deepfake_detection_model.keras")
# model = tf.keras.models.load_model(model_path)

# Model loading
MODEL_PATH = "models/deepfake_detection_model.keras"

def download_model():
    if not os.path.exists(MODEL_PATH):
        logger.info("Downloading model from GCS...")
        try:
            bucket = client.bucket("alethia_model")
            blob = bucket.blob("deepfake_detection_model.keras")
            if not blob.exists():
                logger.error("Model file does not exist in GCS bucket")
                raise RuntimeError("Model file does not exist in GCS bucket")
            os.makedirs("models", exist_ok=True)
            blob.download_to_filename(MODEL_PATH)
            logger.info("Model downloaded successfully")
        except Exception as e:
            logger.error(f"Failed to download model: {e}")
            raise RuntimeError(f"Failed to download model: {e}")
    else:
        logger.info("Model already exists locally")

# Load model at startup
download_model()
model = tf.keras.models.load_model(MODEL_PATH)
logger.info("Model loaded successfully")

# Define constants
FRAME_COUNT = 10
FRAME_SIZE = (128, 128)

def preprocess_video(video_path):
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
    port = int(os.getenv("PORT", 8080))  # Use Render's PORT or default to 8080
    uvicorn.run(app, host="0.0.0.0", port=port)