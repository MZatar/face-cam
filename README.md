# FaceCam Widget
A lightweight, borderless desktop webcam widget built with Python and OpenCV. Perfect for screen recording, presentations, or streaming without a bulky UI getting in the way.

## Features
* **Borderless & Draggable:** Click and drag anywhere to move.
* **Scroll Opacity:** Scroll the mouse wheel over the camera to change transparency.
* **Dynamic Sizing:** Right-click to cycle through sizes.
* **Auto-Save:** Remembers your position, size, and opacity between launches.

## How to Use
Download the standalone `.exe` from the [Releases](../../releases) tab and run it. No Python installation required.

### Controls
* **Left Click & Drag:** Move the widget.
* **Right Click:** Cycle sizes (Large, Medium, Small).
* **Mouse Wheel:** Adjust transparency.
* **`R`:** Reset to center screen, 100% opacity, and default size.
* **Middle Click / `ESC`:** Close the app.

## Build from Source
1. Clone the repo.
2. Install dependencies: `pip install opencv-python Pillow`
3. Run: `python face-cam.py`
