# 🛡️ Wall Guard

Real-time person detection near your wall/fence using YOLOv8 + zone-based monitoring.

## Features
- 🔍 Detects people in a configurable zone (wall area)
- 📊 Live count display
- 🚨 Alert when threshold exceeded (screenshot + JSON log)
- 📸 Save zone screenshot with `z` key
- 📝 JSON event logging
- 🎥 Supports webcam & IP cameras (RTSP)

## Quick Start

```bash
# 1. Clone
git clone https://github.com/masimmirzaisi100-art/wall-guard.git
cd wall-guard

# 2. Install
pip install -r requirements.txt

# 3. Configure (edit config.yaml - set your camera & zone)
nano config.yaml

# 4. Run
python main.py   
