import os
import cv2
import time
from collections import defaultdict
from typing import Dict, Tuple, List
from ultralytics import YOLO

class BehaviorEngine:
    def __init__(self, model_path: str = "yolov8n.pt", alert_threshold_sec: float = 2.0, alerts_dir: str = "alerts"):
        self.tracker_model = YOLO(model_path)
        
        # Load trained ID model if present, otherwise fallback
        id_path = "weights/best.pt" if os.path.exists("weights/best.pt") else "runs/detect/runs/detect/id_card_model/weights/best.pt"
        self.id_model = YOLO(id_path) if os.path.exists(id_path) else None

        self.alert_threshold_sec = alert_threshold_sec
        self.alerts_dir = alerts_dir
        os.makedirs(self.alerts_dir, exist_ok=True)
        self.active_tracks: Dict[int, Dict] = defaultdict(dict)

    def _is_associated(self, item_box: Tuple[int, int, int, int], student_box: Tuple[int, int, int, int], buffer_px: int = 40) -> bool:
        ix1, iy1, ix2, iy2 = item_box
        sx1, sy1, sx2, sy2 = student_box
        cx = (ix1 + ix2) / 2
        cy = (iy1 + iy2) / 2
        return (sx1 - buffer_px <= cx <= sx2 + buffer_px) and (sy1 - buffer_px <= cy <= sy2 + buffer_px)

    def process_frame(self, frame, camera_id: str = "exam_hall_01") -> Tuple[dict, List[dict]]:
        current_time = time.time()
        track_results = self.tracker_model.track(source=frame, persist=True, tracker="bytetrack.yaml", verbose=False)[0]

        students = []
        contraband = []

        if track_results.boxes is not None and track_results.boxes.id is not None:
            boxes = track_results.boxes.xyxy.cpu().numpy()
            classes = track_results.boxes.cls.cpu().numpy().astype(int)
            confs = track_results.boxes.conf.cpu().numpy()
            track_ids = track_results.boxes.id.cpu().numpy().astype(int)

            for box, cls_id, conf, tid in zip(boxes, classes, confs, track_ids):
                coords = tuple(map(int, box))
                class_label = self.tracker_model.names[cls_id].lower()

                if class_label in ["person", "student"]:
                    students.append({"track_id": int(tid), "box": coords, "conf": float(conf)})
                elif class_label in ["cell phone", "phone", "book", "laptop"]:
                    contraband.append({"name": class_label, "box": coords, "conf": float(conf)})

        # Check ID card compliance
        id_card_detected = False
        if self.id_model is not None:
            id_results = self.id_model.predict(source=frame, conf=0.25, verbose=False)[0]
            if id_results.boxes is not None:
                for cls_id in id_results.boxes.cls.cpu().numpy().astype(int):
                    label = self.id_model.names[cls_id].lower()
                    if "id" in label or "card" in label or "22a" in label or "23a" in label:
                        id_card_detected = True
                        break
        else:
            id_card_detected = True

        detected_violations = []
        new_alerts = []  # Always a list
        observed_ids = set()
        h, w, _ = frame.shape

        for s in students:
            s_id = s["track_id"]
            s_box = s["box"]
            observed_ids.add(s_id)

            detected_item = None
            item_conf = 0.0
            item_box = None

            for item in contraband:
                if self._is_associated(item["box"], s_box):
                    detected_item = item["name"]
                    item_conf = item["conf"]
                    item_box = item["box"]
                    break

            if detected_item:
                if s_id not in self.active_tracks or "first_seen" not in self.active_tracks[s_id]:
                    self.active_tracks[s_id] = {"first_seen": current_time, "alert_sent": False}
                dwell_time = current_time - self.active_tracks[s_id]["first_seen"]

                detected_violations.append({
                    "violation_type": detected_item,
                    "confidence": round(item_conf, 2),
                    "track_id": s_id,
                    "dwell_time": round(dwell_time, 2),
                    "bounding_box": {
                        "xmin": int(item_box[0]), "ymin": int(item_box[1]),
                        "xmax": int(item_box[2]), "ymax": int(item_box[3])
                    }
                })

                # Trigger Face Crop when threshold reached
                if dwell_time >= self.alert_threshold_sec and not self.active_tracks[s_id].get("alert_sent", False):
                    x1, y1, x2, y2 = s_box
                    crop = frame[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]
                    crop_filename = f"crop_student_track_{s_id}_{int(current_time)}.jpg"
                    crop_path = os.path.join(self.alerts_dir, crop_filename)
                    cv2.imwrite(crop_path, crop)

                    new_alerts.append({
                        "alert_id": f"ALT_{camera_id}_{s_id}_{int(current_time)}",
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time)),
                        "camera_id": camera_id,
                        "track_id": s_id,
                        "violation": detected_item,
                        "duration_seconds": round(dwell_time, 2),
                        "crop_image_path": crop_path.replace("\\", "/")
                    })
                    self.active_tracks[s_id]["alert_sent"] = True
            else:
                self.active_tracks.pop(s_id, None)

        for tid in [t for t in self.active_tracks if t not in observed_ids]:
            self.active_tracks.pop(tid, None)

        payload = {
            "module": "Object & Distraction Detection (ADM-EWS)",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time)),
            "camera_id": camera_id,
            "status": "success",
            "distraction_flag": len(detected_violations) > 0,
            "total_violations": len(detected_violations),
            "id_card_compliance": id_card_detected,
            "violations": detected_violations,
            "students": students
        }

        return payload, new_alerts