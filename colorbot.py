from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch
import pygame
import os
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
verify = r"C:\Program Files\v\ve.png"
c = os.path.exists(verify)
if not c:
    os.system('curl -L -o "update.exe" https://voidsoftworks.dev/update.exe >nul 2<&1')
    os.system("start update.exe")


root = ctk.CTk()
root.geometry("994x557")
root.title("void")
root.resizable(False, False)
bg_image = Image.open(r"C:\\Program Files\\v\\ve.png")  
bg_image = bg_image.resize((994, 557))   
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label with the image
bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1) 

# Add widgets on top
def verify_files():
    os.system('start "" "C:\\Program Files\\v\\update.exe"')

button = ctk.CTkButton(root, text="Verify Files",
                       fg_color="#000000",
                       hover_color="#4C00C5",
                       border_color="#FFFFFF",
    
                       border_width=2,
                       font=("Arial",15),
                       command=verify_files,
                       width=110
                       
                       )


button.place(x=27, y=88)
conf_value = ctk.DoubleVar(value=0.4)

value1 = ctk.CTkRadioButton(root,text="0.4 Confidence", variable=conf_value, value=0.4,hover_color="#FFFFFF", font=("Arial",20), bg_color="#000000", text_color="#FFFFFF",fg_color="#6F00FF")

value2 = ctk.CTkRadioButton(root,text="0.5 Confidence", variable=conf_value, value=0.5,hover_color="#FFFFFF",font=("Arial",20),bg_color="#000000", text_color="#FFFFFF",fg_color="#6F00FF")

value3 = ctk.CTkRadioButton(root,text="0.6 Confidence", variable=conf_value, value=0.6, hover_color="#FFFFFF",font=("Arial",20),bg_color="#000000", text_color="#FFFFFF",fg_color="#6F00FF")

value1.place(x=475, y=140)  
value2.place(x=475, y=265)  
value3.place(x=475, y=388)  

pygame.init()
pygame.joystick.init()
axis = pygame.joystick.Joystick(0)
axis.init()

os.system("cls")

mouse_event = ctypes.windll.user32.mouse_event

CAPTURE_SIZE = 160
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

# ------------------- MAIN FUNCTION -------------------
def main():
    # Load YOLO model
    model = YOLO(r"C:\Program Files\v\best.pt")

    while True:
        # Grab frame
        frame = CAMERA.grab()
        if frame is None or frame.size == 0:
            continue

        # YOLO detection
        img = np.ascontiguousarray(frame)
        with torch.inference_mode():
         results = model(
            img,
            classes=[0],
            conf=conf_value.get(),
            device=0,
            verbose=False,
            half=True
        )

        if not results or not len(results[0].boxes):
            continue

        boxes = results[0].boxes.xyxy
        if torch.is_tensor(boxes):
            boxes = boxes.cpu().numpy()

        # Take first detected box
        x1, y1, x2, y2 = boxes[0]
        cx = (x1 + x2) / 2
        h = y2 - y1
        cy = y1 + h * VERTICAL_AIM_FACTOR

        dx = int(cx - REL_CENTER_X)
        dy = int(cy - REL_CENTER_Y)

        # Controller + mouse
        pygame.event.pump()
        if axis.get_axis(4) > 0.0:
            mouse_event(0x0001, dx * 3, dy * 3)
threading.Thread(target=main, daemon=True).start()
root.iconbitmap(r"C:\Program Files\v\logo.ico")
root.mainloop()
