from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch
import pygame
import os
import time
import customtkinter as ctk

pygame.init()
axis = pygame.joystick.Joystick(0)
pygame.joystick.init()
axis.init()

os.system("cls")

try:
 DEVICE = "cuda"  
 if DEVICE == "cuda":
    torch.backends.cudnn.benchmark = True

 mouse_event = ctypes.windll.user32.mouse_event
 print("\nThe Lower The Res The Faster But Worse Close Range Less Screen Pixels Can't See")
 print("[1] 160x160")
 print("[2] 256x256")
 print("[3] 300x300")
 print("[4] 224x224")
 print("[5] 192x192")
 print("[6] 356x356")

 res = input("Pick A Res")
 
 if res == "1":
    CAPTURE_SIZE = 160
 if res == "2":
    CAPTURE_SIZE = 256
 if res == "3":
    CAPTURE_SIZE = 300
 if res == "4":
    CAPTURE_SIZE = 224
 if res == "5":
    CAPTURE_SIZE = 192
 if res == "3":
    CAPTURE_SIZE = 356


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
 


 class PersonDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)


    @torch.inference_mode()
    def detect_person(self, img):
        img = np.ascontiguousarray(img)
        
        value = 0.1
        ctk.set_default_color_theme("green")
        ctk.set_appearance_mode("dark")

        app = ctk.CTk()
        app.geometry("900x160")
        app.title("void")

        label = ctk.CTkLabel(app, text=f"Strength & Also The Higher The More False Positives It Blocks Out {value}")
        label.pack(pady=10)
        def callme(c):
         global value
         value = float(c)
         label.configure(text=f"Strength & Also The Higher The More False Positives It Blocks Out {value}")
           
        slider = ctk.CTkSlider(app, from_=0.1, to=1, command=callme)
        slider.set(value)

        slider.pack(pady=20)

        app.mainloop()
        
        results = self.model(
            img,
            classes=[0],           
            conf=value,           
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
         mouse_event(0x0001, dx, dy)

except Exception as file_err:
    print("Error Please Reinstall from the install.exe or Plug in controller")


def banner():
 print("""
     \033[1;35m                   
  _   __     _    __
 | | / /__  (_)__/ /
 | |/ / _ \/ / _  / 
 |___/\___/_/\_,_/  v14 """)
 print("\033[0m[\033[1;34mINFO\033[0m] Loaded")
 main()
banner
