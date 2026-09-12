import cv2
import json
from behavior_engine import BehaviorEngine

def run_video_demo(video_path="demo.mp4"):
    engine = BehaviorEngine(model_path="yolov8n.pt", alert_threshold_sec=2.0)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Cannot open {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    print(f"Streaming '{video_path}'. Press 'q' inside video window to exit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        data, alerts = engine.process_frame(frame, camera_id="exam_hall_01")

        # Safely loop through alerts (empty list when none, dicts when triggered)
        if alerts:
            for alert in alerts:
                print("\n🚨 [ALERT DISPATCHED TO FACE RECOGNITION] 🚨")
                print(json.dumps(alert, indent=2))

        # 1. Draw Green bounding boxes for all students
        for s in data.get("students", []):
            x1, y1, x2, y2 = s["box"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Student ID: {s['track_id']}", (x1, max(20, y1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 2. Draw Red bounding boxes for any active violations (phone)
        for v in data.get("violations", []):
            b = v["bounding_box"]
            cv2.rectangle(frame, (b["xmin"], b["ymin"]), (b["xmax"], b["ymax"]), (0, 0, 255), 2)
            cv2.putText(frame, f"VIOLATION: {v['violation_type']} ({v['dwell_time']}s)",
                        (b["xmin"], max(25, b["ymin"] - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Campus AI - Object & Behavior Analysis", frame)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_video_demo("videi.mp4")