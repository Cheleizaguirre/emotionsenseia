EmotionSense AI

Real-time facial emotion recognition desktop application built with Python 3.11, OpenCV, and FER (MTCNN). The system captures live video from a webcam, detects faces, and classifies emotions with confidence scoring and buffered smoothing for improved stability.

🎯 Purpose

Detect human emotions in real time using computer vision and AI.

Provide an intuitive graphical interface for live visualization.

Improve accuracy through confidence thresholds and emotion buffering.

Track emotion history for short-term behavioral analysis.

✨ Key Features

Real-time face detection via webcam.

Emotion classification (happy, sad, angry, fear, surprise, neutral, disgust).

Confidence percentage display.

Buffered emotion smoothing to reduce flickering results.

Live emotion sidebar indicator.

Emotion history log with timestamps.

Modern UI built with ttkbootstrap.

🛠️ Stack
Layer	Technology
Language	Python 3.11
Computer Vision	OpenCV
Emotion Recognition	FER + MTCNN
GUI Framework	Tkinter + ttkbootstrap
Image Processing	PIL (Pillow)
Data Handling	NumPy
⚙️ Local Installation (Developers)
# 1. Clone repository
$ git clone https://github.com/yourusername/emotionsenseai.git
$ cd emotionsenseai

# 2. Create virtual environment (recommended)
$ python -m venv venv
$ source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Run application
$ python main.py


Note: Make sure your device has a working webcam. Some systems may require additional OpenCV or camera permissions.

🧠 How It Works

The webcam captures live frames.

Frames are processed using OpenCV.

FER with MTCNN detects faces and predicts emotion probabilities.

A confidence threshold filters weak predictions.

A small emotion buffer determines the most frequent emotion to improve stability.

Results are displayed in the interface with percentage and history log.

🚀 Future Improvements

Export emotion history to CSV.

Multi-face simultaneous tracking.

Cloud-based emotion analytics dashboard.

Model customization and retraining.

🤝 Contributing

Fork the repository and create a new branch (feature/YourFeature).

Commit changes with clear messages.

Open a Pull Request describing your improvements.
