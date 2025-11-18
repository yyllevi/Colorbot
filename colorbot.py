from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch

# ---------------- GPU Setup ----------------
DEVICE = "cuda"  # you want GPU
print(f"[INFO] Using device: {DEVICE}")
if DEVICE == "cuda":
    torch.backends.cudnn.benchmark = True

mouse_event = ctypes.windll.user32.mouse_event

# ---------------- Capture Config -------------------
FULL_CENTER_X = 960
FULL_CENTER_Y = 540

CAPTURE_SIZE = 320  # 320x320 FOV

REL_CENTER_X = CAPTURE_SIZE // 2
REL_CENTER_Y = CAPTURE_SIZE // 2

REGION = (
    FULL_CENTER_X - REL_CENTER_X,  # left
    FULL_CENTER_Y - REL_CENTER_Y,  # top
    FULL_CENTER_X + REL_CENTER_X,  # right
    FULL_CENTER_Y + REL_CENTER_Y,  # bottom
)

CAMERA = bettercam.create(
    output_idx=0,
    output_color="BGR",
    region=REGION
)

if CAMERA is None:
    raise RuntimeError(f"BetterCam failed to initialize. REGION={REGION}")


# ---------------- YOLO Loader -------------------
class PersonDetector:
    def __init__(self, model_path):
        print(f"[INFO] Loading PyTorch model: {model_path}")
        self.model = YOLO(model_path)
        self.model.to(DEVICE)  # GPU

    @torch.inference_mode()
    def detect_person(self, img):
        img = np.ascontiguousarray(img)

        results = self.model(
            img,
            classes=[0],           # person
            conf=0.5,              # tweak if needed for dummy
            imgsz=CAPTURE_SIZE,    # roughly match FOV
            device=DEVICE,
            half=True,             # FP16
            verbose=False
        )

        if not results or not len(results[0].boxes):
            return []

        return results[0].boxes.xyxy  # tensor (N, 4)


# ---------------- Capture -------------------
def grab():
    frame = CAMERA.grab()
    if frame is None:
        return np.array([])
    return frame  # already BGR from bettercam


# ---------------- Main Loop -----------------------
def main():
    detector = PersonDetector("siva.pt")

    VERTICAL_AIM_FACTOR = 0.25  # 0 = feet, 1 = head-ish

    while True:
        img = grab()
        if img.size == 0:
            continue

        boxes = detector.detect_person(img)
        if len(boxes) == 0:
            continue

        if torch.is_tensor(boxes):
            boxes = boxes.cpu().numpy()

        # -------- FIRST BOX ONLY --------
        x1, y1, x2, y2 = boxes[0]

        cx = (x1 + x2) / 2
        h = y2 - y1
        cy = y1 + h * VERTICAL_AIM_FACTOR

        dx = int(cx - REL_CENTER_X)
        dy = int(cy - REL_CENTER_Y)

        # raw hard lock (no smoothing, no closest checks)
        mouse_event(0x0001, dx, dy)


if __name__ == "__main__":
    main()
