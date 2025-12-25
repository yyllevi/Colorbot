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

root = ctk.CTk()
root.geometry("957x538")
root.title("void")
root.resizable(False, False)
bg_image = Image.open(r"C:\\Program Files\\v\\gui.png")  
bg_image = bg_image.resize((957, 538))   
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1) 


def openai():
    fp = filedialog.askopenfilename(title="open ai custom .pt file", filetypes=[("",".engine")])
    if fp:
        global ai
        ai = fp 


def verify_files():
    os.system('start "" "C:\\Program Files\\v\\update.exe"')
    time.sleep(2)
    exit()
def default_ai():   
    global ai
    ai = r"C:\Program Files\v\best.engine"

default_ai()

button = ctk.CTkButton(root, text="Verify Files",
                       fg_color="#000000",
                       bg_color="#000000",
                       hover_color="#000000",
                       font=("Arial",17),
                       command=verify_files,
                       width=70,     
                                    
                       )
default = ctk.CTkButton(root, text="Use default ai",
                       fg_color="#000000",
                       hover_color="#000000",
                       command=default_ai,
                       bg_color="#000000",
                       font=("Arial",15),
                       width=70,
                       
                       
                                             )




button.place(x=26, y=74)

default.place(x=23, y=147)


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
    corner_radius=1,
    width=35,
    height=20,
)

files.place(x=16, y=495)

ico = ctk.CTkImage(
    Image.open(r"C:\\Program Files\\v\\save.png"),
    size=(18, 20)
)

save = ctk.CTkButton(
    bg_label,          
    text="",
    image=ico,
    fg_color="#000000",
    hover_color="#000000",
    command=openai,
    border_width=0,
    corner_radius=1,
    width=30,
    height=20,
)

save.place(x=907, y=495)

conf_value = ctk.DoubleVar(value=0.3)

value1 = ctk.CTkRadioButton(root,text="", variable=conf_value, value=0.3,hover_color="#D400FF", font=("Arial",20), bg_color="#000000", text_color="#FFFFFF",fg_color="#3700FF", width=0)

value2 = ctk.CTkRadioButton(root,text="", variable=conf_value, value=0.4,hover_color="#D400FF",font=("Arial",20),bg_color="#000000", text_color="#FFFFFF",fg_color="#3700FF",width=0)

value3 = ctk.CTkRadioButton(root,text="", variable=conf_value, value=0.6, hover_color="#D400FF",font=("Arial",20),bg_color="#000000", text_color="#FFFFFF",fg_color="#3700FF",width=0)

value1.place(x=370, y=141)  
value2.place(x=370, y=265)  
value3.place(x=370, y=395)  

check_ai = ctk.CTkLabel(root, text="", fg_color="#000000", font=("arial", 15, "bold"), bg_color="#000000", text_color="#3700FF")

def own():
 cha = r"C:\Program Files\v\best.engine"
 if ai == cha:
    check_ai.configure(text="Running default ai")
    check_ai.place(x=15, y=215)
 else:
    check_ai.configure(text="Running custom ai")
    check_ai.place(x=15, y=215)
 root.after(100,own)
own()


pygame.init()
pygame.joystick.init()
axis = pygame.joystick.Joystick(0)
axis.init()

os.system("cls")

mouse_event = ctypes.windll.user32.mouse_event

CAPTURE_SIZE = 128
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

        img = np.ascontiguousarray(frame)
        with torch.inference_mode():
         results = model(
            img,
            classes=[0],
            conf=conf_value.get(),
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
threading.Thread(target=main, daemon=True).start()
root.iconbitmap(r"C:\Program Files\v\logo.ico")
root.mainloop()
