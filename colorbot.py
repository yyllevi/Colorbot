from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch
import pygame
import os

pygame.init()
pygame.joystick.init()
axis = pygame.joystick.Joystick(0)
axis.init()

os.system("cls")

mouse_event = ctypes.windll.user32.mouse_event

CAPTURE_SIZE = 187
FULL_CENTER_X = 960
FULL_CENTER_Y = 540
REL_CENTER_X = CAPTURE_SIZE
REL_CENTER_Y = CAPTURE_SIZE
VERTICAL_AIM_FACTOR = 0.25

REGION = (
    FULL_CENTER_X - REL_CENTER_X,
    FULL_CENTER_Y - REL_CENTER_Y,
    FULL_CENTER_X + REL_CENTER_X,
    FULL_CENTER_Y + REL_CENTER_Y,
)

CAMERA = bettercam.create(
    output_idx=0,
    output_color="BGR",
    region=REGION
)


def main():
    model = YOLO(r"C:\v\best.engine")
    while True:
        frame = CAMERA.grab()
        if frame is None or frame.size == 0:
            continue

        img = np.ascontiguousarray(frame)
        with torch.inference_mode():
         results = model(
            img,
            classes=[0],
            conf=0.6,
            device=0,
            verbose=False,
            half=True,
        )

        if not results or not len(results[0].boxes):
            continue

        boxes = results[0].boxes.xyxy
        if torch.is_tensor(boxes):
            boxes = boxes.cpu().numpy()

        x1, y1, x2, y2 = boxes[0]
        cx = (x1 + x2) / 2
        h = y2 - y1
        cy = y1 + h * VERTICAL_AIM_FACTOR

        dx = int(cx - REL_CENTER_X)
        dy = int(cy - REL_CENTER_Y)

        pygame.event.pump()
        if axis.get_axis(4) > 0.0:
            mouse_event(0x0001, (dx * 3), (dy * 3))
main()
