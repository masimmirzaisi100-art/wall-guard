# Wall Guard

Real-time person detection near your wall/fence using YOLOv8.

**Repo:** https://github.com/masimmirzaisi100-art/wall-guard

---

## Installation

### Windows

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

Ubuntu / Linux
sudo apt install -y python3-venv python3-pip libgl1-mesa-glx libglib2.0-0
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

macOS
brew install python@3.11
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py



Google Cloud Shell — Wall Guard Setup
Cloud Shell kholo: https://shell.cloud.google.com/
Phir ye commands ek ek karke run karo:
Cell 1 — System Dependencies
sudo apt-get update && sudo apt-get install -y python3-venv python3-pip libgl1-mesa-glx libglib2.0-0
Cell 2 — Clone Project
git clone https://github.com/masimmirzaisi100-art/wall-guard.git
cd wall-guard
Cell 3 — Virtual Environment
python3 -m venv venv
source venv/bin/activate
Cell 4 — Install Dependencies
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics opencv-python-headless numpy pyyaml
Cell 5 — Verify
python -c "from ultralytics import YOLO; print('OK')"
Output aana chahiye:
OK
Cell 6 — Test with Image
wget -q https://ultralytics.com/images/bus.jpg
python -c "
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
results = model.predict('bus.jpg', classes=[0], conf=0.5)
print(f'People detected: {len(results[0].boxes)}')
"
Cell 7 — RTSP Camera Test (Agar aapka camera internet pe hai)
python -c "
from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture('rtsp://username:password@camera-ip:554/stream')
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        model = YOLO('yolov8n.pt')
        results = model.predict(frame, classes=[0], conf=0.5)
        print(f'People: {len(results[0].boxes)}')
        cv2.imwrite('result.jpg', frame)
else:
    print('Camera not accessible')
cap.release()
"
rtsp://username:password@camera-ip:554/stream — apna URL daalo
Directory (Cloud Shell mein kya hoga)
/home/username/wall-guard/
├── main.py
├── config.yaml
├── requirements.txt
├── venv/
├── zones/
└── logs/
File Name
main.py
Path: /home/username/wall-guard/main.py
Important
Cheez	Detail
Camera	Cloud Shell mein physical camera nahi hai — sirf RTSP URL kaam karega
Display	cv2.imshow() nahi chalega — sirf cv2.imwrite() (screenshot save)
Session close	Data delete ho jayega — git push karo agar save karna ho
GPU	Cloud Shell mein GPU nahi hai — CPU pe ~5-8 FPS

