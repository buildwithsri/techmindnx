import os
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form
from behavior_engine import BehaviorEngine

app = FastAPI(
    title="Module 05: Smart Campus Surveillance & Object Detection API",
    description="Real-time student behavior monitoring, contraband detection, and ID-card compliance microservice."
)

# Initialize engine once on startup
engine = BehaviorEngine(alert_threshold_sec=2.0)

@app.get("/")
def health_check():
    return {
        "service": "05_object_detection",
        "status": "online",
        "version": "1.0.0"
    }

@app.post("/analyze-frame")
async def analyze_frame(
    camera_id: str = Form("exam_hall_01"),
    file: UploadFile = File(...)
):
    # Read uploaded image bytes directly into OpenCV format
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"status": "error", "message": "Invalid image payload"}

    # Process through detection, tracking, spatial association, and ID checks
    academic_payload, face_alerts = engine.process_frame(frame, camera_id=camera_id)

    return {
        "status": "success",
        "academic_report": academic_payload,
        "face_alerts": face_alerts
    }