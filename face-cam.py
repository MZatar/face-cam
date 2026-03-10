import os
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from pathlib import Path

APP_DIR = Path(os.getenv('APPDATA')) / "FaceCam"
SETTINGS_FILE_PATH = APP_DIR / "window_settings.txt"

FRAME_WIDTH, FRAME_HEIGHT, FPS = 1920, 1080, 30
FRAME_UPDATE_INTERVAL_MS = int(1000 / FPS)

class FaceCam:
    def __init__(self):
        self.root = tk.Tk()
        self.sizes = [(768, 432), (512, 288), (256, 144), (512, 288)]
        self.size_index = 1
        
        self.load_settings()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        self.lbl = tk.Label(self.root, bd=0, highlightthickness=2, highlightbackground="yellow")
        self.lbl.pack(fill=tk.BOTH, expand=tk.YES)

        self.lbl.bind("<ButtonPress-1>", self.start_move)
        self.lbl.bind("<ButtonRelease-1>", self.stop_move)
        self.lbl.bind("<B1-Motion>", self.do_move)
        self.lbl.bind("<Enter>", lambda e: self.lbl.bind_all("<MouseWheel>", self.on_mouse_wheel))
        self.lbl.bind("<Leave>", lambda e: self.lbl.unbind_all("<MouseWheel>"))
        self.lbl.bind("<Button-2>", lambda e: self.root.destroy())
        self.lbl.bind("<Button-3>", self.change_size)
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<r>", self.reset_settings)
        self.root.bind("<R>", self.reset_settings)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)

        self._alpha = self.root.attributes('-alpha') or 1.0
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, self.sizes[self.size_index])
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.lbl.imgtk = imgtk
            self.lbl.configure(image=imgtk)
        self.root.after(FRAME_UPDATE_INTERVAL_MS, self.update_frame)

    def start_move(self, event):
        self.root.x, self.root.y = event.x, event.y

    def stop_move(self, event):
        self.save_settings()

    def do_move(self, event):
        x, y = event.x_root - self.root.x, event.y_root - self.root.y
        self.root.geometry(f"+{x}+{y}")

    def on_mouse_wheel(self, event):
        delta = event.delta / 1200
        self._alpha = max(0.1, min(1.0, self._alpha + delta))
        self.root.attributes('-alpha', self._alpha)
        self.save_settings()

    def save_settings(self):
        APP_DIR.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE_PATH, "w") as f:
            f.write(f"{self.root.geometry()}\n{self._alpha}\n{self.size_index}\n")

    def load_settings(self):
        try:
            with open(SETTINGS_FILE_PATH, "r") as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    self.root.geometry(lines[0].strip())
                    self._alpha = float(lines[1].strip())
                    self.root.attributes('-alpha', self._alpha)
                    self.size_index = int(lines[2].strip())
        except (FileNotFoundError, ValueError):
            pass

        width, height = self.sizes[self.size_index]
        self.root.geometry(f"{width}x{height}")

    def change_size(self, event):
        old_width, old_height = map(int, self.root.geometry().split("+")[0].split("x"))
        old_center_x = self.root.winfo_rootx() + old_width // 2
        old_center_y = self.root.winfo_rooty() + old_height // 2

        self.size_index = (self.size_index + 1) % len(self.sizes)
        new_width, new_height = self.sizes[self.size_index]
        new_x, new_y = old_center_x - new_width // 2, old_center_y - new_height // 2

        self.root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
        self.save_settings()

    def reset_settings(self, event=None):
        self.size_index = 1
        self._alpha = 1.0
        self.root.attributes('-alpha', self._alpha)
        width, height = self.sizes[self.size_index]
        
        # Snap to screen center
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.save_settings()

    def run(self):
        self.root.mainloop()
        self.cap.release()

if __name__ == "__main__":
    FaceCam().run()