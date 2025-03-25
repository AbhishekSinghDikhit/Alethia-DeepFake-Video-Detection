from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import tempfile
import tensorflow as tf
import uvicorn
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the deepfake detection model
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
model_path = os.path.join(base_dir, "models", "deepfake_detection_model.keras")
model = tf.keras.models.load_model(model_path)

# Define constants
FRAME_COUNT = 10  # Model expects exactly 10 frames per video
FRAME_SIZE = (128, 128)  # Resize frames to 128x128

def preprocess_video(video_path):
    """Extracts exactly FRAME_COUNT frames, resizes them, and normalizes them."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames < FRAME_COUNT:
        return None  # Not enough frames to process

    frame_indices = np.linspace(0, total_frames - 1, FRAME_COUNT, dtype=int)

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, FRAME_SIZE)  # Resize to (128,128)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frame = frame / 255.0  # Normalize pixel values
        frames.append(frame)

    cap.release()

    if len(frames) != FRAME_COUNT:
        return None  # Ensure exactly FRAME_COUNT frames

    return np.expand_dims(np.array(frames), axis=0)  # Shape: (1, FRAME_COUNT, 128, 128, 3)

@app.post("/detect/")
async def detect_deepfake_video(file: UploadFile = File(...)):
    try:
        # Save the video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(await file.read())
            video_path = temp_file.name

        # Preprocess video frames
        video_frames = preprocess_video(video_path)
        if video_frames is None:
            return {"error": "Not enough frames extracted or video processing failed."}

        # Ensure the correct shape
        print(f"Input shape to model: {video_frames.shape}")  # Debugging

        # Predict using the model
        prediction = model.predict(video_frames)[0]  # Get first sample prediction
        real_score, deepfake_score = prediction  # Assuming softmax output

        return {
            "deepfake": bool(deepfake_score > real_score),
            "scores": {"real": float(real_score), "deepfake": float(deepfake_score)},
        }

    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}

# Run Uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
