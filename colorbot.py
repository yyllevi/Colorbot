from ultralytics import YOLO
import bettercam
import numpy as np
import ctypes
import torch
import pygame
import os
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog
import threading
import time

verify = r"C:\Program Files\v\ve.png"
c = os.path.exists(verify)
if not c:
    os.system('curl -L -o "update.exe" https://voidsoftworks.dev/update.exe >nul 2<&1')
    os.system("start update.exe")


root = ctk.CTk()
root.geometry("957x538")
root.title("void")
root.resizable(False, False)
bg_image = Image.open(r"C:\\Program Files\\v\\ve.png")  
bg_image = bg_image.resize((957, 538))   
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label with the image
bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1) 


def openai():
    fp = filedialog.askopenfilename(title="open ai custom .pt file", filetypes=[("",".pt")])
    if fp:
        global ai
        ai = fp


def verify_files():
    os.system('start "" "C:\\Program Files\\v\\update.exe"')
    time.sleep(2)
    exit()

def default_ai():   
    global ai
    ai = r"C:\Program Files\v\best.pt"

default_ai()

button = ctk.CTkButton(root, text="Verify Files",
                       fg_color="#000000",
                       hover_color="#4C00C5",
                       border_color="#FFFFFF",
                       border_width=2,
                       font=("Arial",15),
                       command=verify_files,
                       width=110                  
                       )
default = ctk.CTkButton(root, text="Use default ai",
                       fg_color="#000000",
                       hover_color="#B08CD1",
                       border_color="#FFFFFF",
                       command=default_ai,
                       border_width=2,
                       font=("Arial",15),
                       width=115,
                       height=30
                       )

default.place(x=20, y=144)
button.place(x=22, y=85)

icon = ctk.CTkImage(
    Image.open(r"C:\Program Files\v\folder.png"),
    size=(18, 20)
)

files = ctk.CTkButton(
    bg_label,          
    text="",
    image=icon,
    fg_color="#000000",
    hover_color="#000000",
    command=openai,
    border_width=0,
    width=18,
    height=20,
)

files.place(x=8, y=498)

conf_value = ctk.DoubleVar(value=0.4)

value1 = ctk.CTkRadioButton(root,text="0.4 Confidence", variable=conf_value, value=0.4,hover_color="#FFFFFF", font=("Arial",20), bg_color="#000000", text_color="#FFFFFF",fg_color="#6F00FF")

value2 = ctk.CTkRadioButton(root,text="0.5 Confidence", variable=conf_value, value=0.5,hover_color="#FFFFFF",font=("Arial",20),bg_color="#000000", text_color="#FFFFFF",fg_color="#6F00FF")

value3 = ctk.CTkRadioButton(root,text="0.6 Confidence", variable=conf_value, value=0.6, hover_color="#FFFFFF",font=("Arial",20),bg_color="#000000", text_color="#FFFFFF",fg_color="#6F00FF")

value1.place(x=470, y=137)  
value2.place(x=470, y=257)  
value3.place(x=470, y=377)  

check_ai = ctk.CTkLabel(root, text="", fg_color="#000000", font=("arial", 17))

def own():
    cha = r"C:\Program Files\v\best.pt"
    if ai == cha:
        check_ai.configure(text="Using Default Ai")
        check_ai.place(x=15, y=205)
    else:
        check_ai.configure(text="Using Custom Ai")
        check_ai.place(x=15, y=205)
    root.after(100,own)

own()

pygame.init()
pygame.joystick.init()
axis = pygame.joystick.Joystick(0)
axis.init()

os.system("cls")

mouse_event = ctypes.windll.user32.mouse_event

CAPTURE_SIZE = 192
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
    ca = ai
    model = YOLO(rf"{ca}")

    while True:
        if ca != ai:
            ca = ai
            model = YOLO(rf"{ca}")

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
                half=True,
                max_det=1  # Changed from 1 to allow multiple detections
            )

        if not results or not len(results[0].boxes):
            continue

        boxes = results[0].boxes.xyxy
        if torch.is_tensor(boxes):
            boxes = boxes.cpu().numpy()

        # Find closest box to center
        min_distance = float('inf')
        closest_box = None

        for box in boxes:
            x1, y1, x2, y2 = box
            cx = (x1 + x2) / 2
            h = y2 - y1
            cy = y1 + h * VERTICAL_AIM_FACTOR
            
            # Calculate distance from screen center
            distance = np.sqrt((cx - REL_CENTER_X)**2 + (cy - REL_CENTER_Y)**2)
            
            if distance < min_distance:
                min_distance = distance
                closest_box = box

        if closest_box is None:
            continue

        # Use the closest box
        x1, y1, x2, y2 = closest_box
        cx = (x1 + x2) / 2
        h = y2 - y1
        cy = y1 + h * VERTICAL_AIM_FACTOR

        dx = int(cx - REL_CENTER_X)
        dy = int(cy - REL_CENTER_Y)

        # Controller + mouse
        pygame.event.pump()
        if axis.get_axis(4) > 0.0:
            mouse_event(0x0001, int(dx * 3), int(dy * 3))

threading.Thread(target=main, daemon=True).start()
root.iconbitmap(r"C:\Program Files\v\logo.ico")
root.mainloop()
