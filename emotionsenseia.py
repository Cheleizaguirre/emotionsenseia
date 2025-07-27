import sys
import types
import time
import tkinter as tk
from tkinter import ttk

try:
    import moviepy.editor as mpy
except ModuleNotFoundError:
    dummy = types.ModuleType("moviepy.editor")
    sys.modules["moviepy.editor"] = dummy

import cv2
import numpy as np
from fer import FER
from PIL import Image, ImageTk, ImageDraw, ImageFont
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from collections import Counter

# Diccionarios de emoticonos y nombres de emociones
emoticons = {
    "angry": "😠", "disgust": "🤢", "fear": "😨",
    "happy": "😊", "sad": "😢", "surprise": "😮", "neutral": "😐"
}
emotion_names = {
    "angry": "Enojado", "disgust": "Asco", "fear": "Miedo",
    "happy": "Feliz", "sad": "Triste", "surprise": "Sorprendido", "neutral": "Neutral"
}

# Inicializamos el detector con MTCNN activado
detector = FER(mtcnn=True)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección de Emociones")
        self.root.geometry("1000x600")

        self.capturing = False
        self.cam = None
        self.last_emotion = None
        self.last_score = 0
        self.last_update_time = time.time()
        self.update_delay = 2  # segundos entre actualizaciones
        self.threshold = 0.7   # mayor sensibilidad
        self.emotion_history = []
        self.emotion_buffer = []  # 🆕 Buffer de emociones

        self.setup_ui()

    def setup_ui(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Sidebar
        sidebar = tb.Frame(self.root, bootstyle="secondary", padding=10)
        sidebar.grid(row=0, column=0, sticky="ns")

        tb.Label(sidebar, text="Emociones", font=("Arial", 18)).pack(pady=(10, 10))

        self.emotion_labels = {}
        for key in emoticons:
            text = f"{emotion_names[key]} {emoticons[key]}"
            label = tb.Label(sidebar, text=text, font=("Arial", 14))
            label.pack(pady=2)
            self.emotion_labels[key] = label

        tb.Separator(sidebar, orient="horizontal").pack(fill="x", pady=10)
        tb.Label(sidebar, text="Historial", font=("Arial", 16)).pack(pady=(5, 5))

        self.history_box = tk.Text(sidebar, width=25, height=10, state="disabled", bg="white")
        self.history_box.pack(pady=5)

        # Main content
        main_frame = tb.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.video_label = ttk.Label(main_frame)
        self.video_label.grid(row=0, column=0)

        control_frame = tb.Frame(main_frame)
        control_frame.grid(row=1, column=0, pady=10)

        self.start_btn = tb.Button(control_frame, text="Activar Cámara", bootstyle=SUCCESS, command=self.start_camera)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = tb.Button(control_frame, text="Detener Cámara", bootstyle=DANGER, state="disabled", command=self.stop_camera)
        self.stop_btn.pack(side="left", padx=5)

    def update_sidebar(self, current_emotion):
        for key, label in self.emotion_labels.items():
            if key == current_emotion:
                label.configure(text=f"> {emotion_names[key]} {emoticons[key]}", foreground="blue", font=("Arial", 14, "bold"))
            else:
                label.configure(text=f"{emotion_names[key]} {emoticons[key]}", foreground="black", font=("Arial", 14))

    def update_history(self, emotion, score):
        entry = f"{time.strftime('%H:%M:%S')} - {emotion_names[emotion]} {emoticons[emotion]} ({int(score*100)}%)"
        self.emotion_history.append(entry)
        if len(self.emotion_history) > 10:
            self.emotion_history.pop(0)
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", tk.END)
        self.history_box.insert(tk.END, "\n".join(self.emotion_history))
        self.history_box.configure(state="disabled")

    def start_camera(self):
        if not self.capturing:
            self.cam = cv2.VideoCapture(0)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 🆕 Mejor resolución
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.capturing = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.update_frame()

    def stop_camera(self):
        if self.capturing:
            self.capturing = False
            if self.cam is not None:
                self.cam.release()
                self.cam = None
            self.video_label.configure(image='')
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def update_frame(self):
        if self.capturing and self.cam is not None:
            ret, frame = self.cam.read()
            if ret:
                # 🆕 Mejora visual del frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                pil_image = Image.fromarray(frame_rgb)
                draw = ImageDraw.Draw(pil_image)

                try:
                    font = ImageFont.truetype("DejaVuSans.ttf", 20)
                except IOError:
                    font = ImageFont.load_default()

                results = detector.detect_emotions(frame_rgb)
                if results:
                    result = results[0]  # Solo primera cara
                    (x, y, w, h) = result["box"]
                    detected_emotion, detected_score = max(result["emotions"].items(), key=lambda item: item[1])

                    if detected_score >= self.threshold:
                        self.emotion_buffer.append((detected_emotion, detected_score))
                        if len(self.emotion_buffer) > 5:
                            self.emotion_buffer.pop(0)

                        # 🆕 Emoción más frecuente del buffer
                        top_emotion = Counter([e for e, s in self.emotion_buffer]).most_common(1)[0][0]
                        top_score = max([s for e, s in self.emotion_buffer if e == top_emotion])

                        current_time = time.time()
                        if (self.last_emotion is None) or (top_emotion != self.last_emotion and (current_time - self.last_update_time) >= self.update_delay):
                            self.last_emotion = top_emotion
                            self.last_score = top_score
                            self.last_update_time = current_time
                            self.update_history(top_emotion, top_score)

                        text = f"{emotion_names[top_emotion]} {emoticons[top_emotion]} ({int(top_score*100)}%)"
                        draw.rectangle([(x, y), (x + w, y + h)], outline=(0, 255, 0), width=2)
                        draw.text((x, y - 30), text, font=font, fill=(255, 0, 0))
                        self.update_sidebar(top_emotion)

                imgtk = ImageTk.PhotoImage(image=pil_image)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            self.root.after(10, self.update_frame)

if __name__ == '__main__':
    app = tb.Window(themename="superhero")
    App(app)
    app.mainloop()
