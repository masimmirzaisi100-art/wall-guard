"""
Wall Guard - Detect how many people are near your wall/fence.
Uses YOLOv8 + zone-based detection.
"""

import cv2
import yaml
import time
import json
import os
from datetime import datetime
from pathlib import Path
from ultralytics import YOLO


class WallGuard:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            self.cfg = yaml.safe_load(f)

        self.model = YOLO(self.cfg["model"])
        self.camera = self.cfg["camera"]
        self.conf = self.cfg["confidence"]
        self.zone = self.cfg["zone"]  # polygon points
        self.alert_threshold = self.cfg["alert_threshold"]
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.last_alert_time = 0
        self.alert_cooldown = self.cfg.get("alert_cooldown_sec", 30)

    def draw_zone(self, frame):
        """Draw the detection zone on frame."""
        pts = [tuple(p) for p in self.zone]
        cv2.polylines(frame, [pts], isClosed=True, color=(255, 165, 0), thickness=2)
        cv2.fillPoly(frame, [pts], (255, 165, 0))
        # Re-draw frame with transparency
        overlay = frame.copy()
        cv2.fillPoly(overlay, [pts], (255, 165, 0))
        cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)
        cv2.polylines(frame, [pts], isClosed=True, color=(255, 165, 0), thickness=2)
        return frame

    def point_in_polygon(self, point, polygon):
        """Check if a point is inside a polygon (ray casting)."""
        x, y = point
        n = len(polygon)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    def detect(self, frame):
        """Run detection and return (frame, count, boxes)."""
        results = self.model.predict(frame, classes=[0], conf=self.conf, verbose=False)
        count = 0
        boxes = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                if self.point_in_polygon((cx, cy), self.zone):
                    count += 1
                    boxes.append((x1, y1, x2, y2, box.conf[0]))
        return frame, count, boxes

    def alert(self, count):
        """Trigger alert when threshold exceeded."""
        now = time.time()
        if count >= self.alert_threshold and (now - self.last_alert_time) > self.alert_cooldown:
            self.last_alert_time = now
            msg = f"⚠️  ALERT: {count} person(s) near wall! {datetime.now().strftime('%H:%M:%S')}"
            print(msg)
            # Save screenshot
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_screenshot(ts, count)
            # Log to JSON
            self.log_event(count)
            # TODO: Add Telegram/WhatsApp/SMS alert here
            # self.send_telegram(msg)

    def save_screenshot(self, timestamp, count):
        """Save current frame as evidence."""
        pass  # Called with frame in main loop

    def log_event(self, count):
        """Log detection event to JSON file."""
        event = {
            "time": datetime.now().isoformat(),
            "person_count": count,
            "alert": count >= self.alert_threshold
        }
        log_file = self.log_dir / "events.json"
        events = []
        if log_file.exists():
            with open(log_file) as f:
                events = json.load(f)
        events.append(event)
        with open(log_file, "w") as f:
            json.dump(events, f, indent=2)

    def run(self):
        """Main loop."""
        cap = cv2.VideoCapture(self.camera)
        if not cap.isOpened():
            print(f"❌ Camera not found: {self.camera}")
            return

        print(f"🚀 Wall Guard started | Camera: {self.camera}")
        print(f"   Threshold: {self.alert_threshold} | Confidence: {self.conf}")
        print(f"   Press 'q' to quit, 'z' to save zone screenshot")
        print("-" * 50)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Draw zone
            frame = self.draw_zone(frame)

            # Detect
            _, count, boxes = self.detect(frame)

            # Draw boxes
            for (x1, y1, x2, y2, conf) in boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"Person {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Status
            status = f"Wall ke paas: {count} insaan"
            color = (0, 0, 255) if count >= self.alert_threshold else (0, 255, 0)
            cv2.putText(frame, status, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # FPS
            fps = cap.get(cv2.CAP_PROP_FPS)
            cv2.putText(frame, f"{fps:.0f} FPS", (10, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            # Alert
            if count >= self.alert_threshold:
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 4), (0, 0, 255), -1)
                cv2.rectangle(frame, (0, frame.shape[2]-4), (frame.shape[1], frame.shape[2]), (0, 0, 255), -1)
                self.alert(count)

            cv2.imshow("Wall Guard", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('z'):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = f"zones/zone_{ts}.jpg"
                os.makedirs("zones", exist_ok=True)
                cv2.imwrite(path, frame)
                print(f"📸 Zone saved: {path}")

        cap.release()
        cv2.destroyAllWindows()
        print("👋 Wall Guard stopped.")


if __name__ == "__main__":
    guard = WallGuard()
    guard.run()   
