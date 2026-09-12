# Module 05: Object & Distraction Detection (ADM-EWS)

Real-time surveillance and behavior analysis microservice for smart exam monitoring. Combines spatial association, temporal dwell-time state tracking, and dual-model inference to detect exam misconduct and verify student ID-card compliance.

---

## Features

- **Dual-Model Inference**:
  - `yolov8n.pt`: Real-time student tracking (via ByteTrack) and unauthorized device/phone detection.
  - `weights/best.pt`: Fine-tuned YOLOv8 model for verifying student ID-card presence on desks.
- **Temporal Dwell-Time Filtering**: Evaluates Euclidean overlap between student coordinates and detected contraband over time (default threshold: 2.0 seconds) to prevent false-positive alerts.
- **Automated Evidence Capture**: Automatically crops and saves bounded student regions to `alerts/` upon violation confirmation.

---

## Inter-Team Interfaces

### 1. Face Recognition (Module 03)
When an anomaly crosses the 2-second dwell threshold, the engine stores an evidence snapshot:
- **Image Location**: `alerts/crop_student_track_{track_id}_{timestamp}.jpg`
- **Handoff Payload**: Contains `track_id`, `violation`, and `crop_image_path` for direct identity embedding extraction.

### 2. Academic Evaluation & Anomaly Engine (Module 04)
Outputs the standardized compliance payload:
```json
{
  "module": "Object & Distraction Detection (ADM-EWS)",
  "timestamp": "2026-09-12T14:30:00Z",
  "camera_id": "exam_hall_01",
  "status": "success",
  "distraction_flag": true,
  "total_violations": 1,
  "id_card_compliance": true,
  "violations": [
    {
      "violation_type": "cell phone",
      "confidence": 0.85,
      "track_id": 2,
      "dwell_time": 2.4,
      "bounding_box": {
        "xmin": 320,
        "ymin": 210,
        "xmax": 405,
        "ymax": 360
      }
    }
  ]
}
