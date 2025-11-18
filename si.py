from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch
import pygame

pygame.init()
axis = pygame.joystick.Joystick(0)
pygame.joystick.init()
axis.init()

def banner():
    print("""
\033[1;35m   _____ _ _                  __         
  / ___/(_|_)   ______ _ ____/ /__ _   __
  \__ \/ / / | / / __ `// __  / _ \ | / /
 ___/ / / /| |/ / /_/ // /_/ /  __/ |/ / 
/____/_/_/ |___/\__,_(_)__,_/\___/|___/  v1
 
 By Limegreen0012""")
banner()
try:
 DEVICE = "cuda"  
 if DEVICE == "cuda":
    torch.backends.cudnn.benchmark = True

 mouse_event = ctypes.windll.user32.mouse_event

 FULL_CENTER_X = 960
 FULL_CENTER_Y = 540

 CAPTURE_SIZE = 320  

 REL_CENTER_X = CAPTURE_SIZE // 2
 REL_CENTER_Y = CAPTURE_SIZE // 2

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

 if CAMERA is None:
    raise RuntimeError(f"BetterCam failed to initialize. REGION={REGION}")

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
            conf=0.49,              
            imgsz=CAPTURE_SIZE,    
            device=DEVICE,
            half=True,            
            verbose=False
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
    detector = PersonDetector(r"C:\Program Files\siv\best.pt")

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
main()
