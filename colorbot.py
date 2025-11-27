from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch
import pygame
import os
import time

os.system("cls")

try:
 DEVICE = "cuda"  
 if DEVICE == "cuda":
    torch.backends.cudnn.benchmark = True

 mouse_event = ctypes.windll.user32.mouse_event

 FULL_CENTER_X = 960
 FULL_CENTER_Y = 540

 CAPTURE_SIZE = 512

 REL_CENTER_X = CAPTURE_SIZE 
 REL_CENTER_Y = CAPTURE_SIZE 

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


 class PersonDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.model.to(DEVICE) 

    @torch.inference_mode()
    def detect_person(self, img):
        img = np.ascontiguousarray(img)

        results = self.model(
            img,
            classes=[0],           
            conf=0.8,             
            imgsz=CAPTURE_SIZE,    
            device=DEVICE,           
            verbose=False,
            half=True
        )

        if not results or not len(results[0].boxes):
            return []

        return results[0].boxes.xyxy 

 def grab():
    frame = CAMERA.grab()
    if frame is None:
        return np.array([])
    return frame  

 def main():
    detector = PersonDetector(r"C:\\Program Files\\siv\\best.pt")

    VERTICAL_AIM_FACTOR = 0.25  

    while True:
        img = grab()
        if img.size == 0:
            continue

        boxes = detector.detect_person(img)
        if len(boxes) == 0:
            continue

        if torch.is_tensor(boxes):
            boxes = boxes.cpu().numpy()
            
        x1, y1, x2, y2 = boxes[0]

        cx = (x1 + x2) / 2
        h = y2 - y1
        cy = y1 + h * VERTICAL_AIM_FACTOR

        dx = int(cx - REL_CENTER_X)
        dy = int(cy - REL_CENTER_Y)
        pygame.init()
        axis = pygame.joystick.Joystick(0)
        pygame.joystick.init()
        axis.init()
        pygame.event.pump()
        if axis.get_axis(4) > 0.0:
         mouse_event(0x0001, dx, dy)

except Exception as file_err:
    print("Error Please Reinstall from the install.exe or Plug in controller")


def banner():
 print("""
     \033[1;35m                   
 _____ _ _         
|   __|_|_|_ _ ___ 
|__   | | | | | .'|
|_____|_|_|\_/|__,| v9 """)
 p = input("\n\033[0mEnter \033[1;36mPasskey\033[0m: \033[1;35m")
 if p == "7816":
     print("\033[0m[\033[1;34mINFO\033[0m] Loaded")
     main()
 else:
    print("no nigga")
    time.sleep(2)
banner()
