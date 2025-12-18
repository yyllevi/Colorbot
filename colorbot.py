from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch
import pygame
import os

pygame.init()
axis = pygame.joystick.Joystick(0)
pygame.joystick.init()
axis.init()

os.system("cls")

try:
 pass

 mouse_event = ctypes.windll.user32.mouse_event
 print("""
     \033[1;35m v21 """)
 print("\n\033[0m[\033[1;34mINFO\033[0m] Loaded")

 print("\033[1;36m[\033[0;36m1\033[0m] 160x160")
 print("\033[1;36m[\033[1;33m\033[0;36m2\033[0m] 256x256")
 print("\033[1;36m[\033[1;33m\033[0;36m3\033[0m] 320x320")
 print("\033[1;36m[\033[1;33m\033[0;36m4\033[0m] 224x224")
 print("\033[1;36m[\033[1;33m\033[0;36m5\033[0m] 192x192")
 print("\033[1;36m[\033[1;33m\033[0;36m6\033[0m] 384x384")
 print("\033[1;36m[\033[1;33m\033[0;36m7\033[0m] 128x128")

 res = input("\nPick A Res >> ")
 
 if res == "1":
    CAPTURE_SIZE = 160
 if res == "2":
    CAPTURE_SIZE = 256
 if res == "3":
    CAPTURE_SIZE = 320
 if res == "4":
    CAPTURE_SIZE = 224
 if res == "5":
    CAPTURE_SIZE = 192
 if res == "6":
    CAPTURE_SIZE = 384
 if res == "7":
    CAPTURE_SIZE = 128


 FULL_CENTER_X = 960
 FULL_CENTER_Y = 540


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
 print("\033[1;33m[1]\033[1;36m 0.4")
 print("\033[1;33m[2]\033[1;36m 0.45")
 print("\033[1;33m[3]\033[1;36m 0.5")
 print("\033[1;33m[4]\033[1;36m 0.55")
 print("\033[1;33m[5]\033[1;36m 0.6")
 print("\033[1;33m[6]\033[1;36m 0.65")
 print("\033[1;33m[7]\033[1;36m 0.7")
 print("\033[1;33m[8]\033[1;36m 0.75")
 print("\033[1;33m[9]\033[1;36m 0.8")
 
 value = input("\n\033[0mFilter >> ")
 if value == "1":
    value=0.4
 if value == "2":
    value=0.45
 if value == "3":
    value=0.5
 if value == "4":
    value=0.55
 if value == "5":
    value=0.6
 if value == "6":
    value=0.65
 if value == "7":
    value=0.7
 if value == "8":
    value=0.75
 if value == "9":
    value=0.8

 class PersonDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    @torch.inference_mode()
    def detect_person(self, img):
        img = np.ascontiguousarray(img)
        results = self.model(
            img,
            classes=[0],           
            conf=value,           
            imgsz=CAPTURE_SIZE,    
            device=0,           
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
    detector = PersonDetector(r"C:\Program Files\v\best.pt")

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
        
        pygame.event.pump()
        if axis.get_axis(4) > 0.0:
         mouse_event(0x0001, int(dx * 2.3), int(dy * 2.3))

except Exception as file_err:
    print("Error Please Reinstall from the install.exe or Plug in controller")

main()
