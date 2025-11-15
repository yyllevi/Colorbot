from mss import mss # by levi && lonely
import numpy as np
import ctypes
import pygame
import os
import time
import cv2

os.system('cls')

left, top = 650, 250
width, height = 380, 380


"""colors"""
h = "\033[38;5;93m"
purple = "\033[1;35m"
red = "\033[1;31m"
purple2 = "\033[0;35m"
gray = "\033[1;30m"
dark_red = "\033[0;31m"
"""colors"""


def main():
 with mss() as ss:
     while True:
      try:
         pygame.init()
         pygame.joystick.init()
         AXIS = pygame.joystick.Joystick(0)
         AXIS.init()
         screen = {"left": left, "top": top, "width": width, "height": height}
         screenshot = np.array(ss.grab(screen))
    
         hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)


         lower = np.array([27, 180, 180])
         upper = np.array([30, 255, 255])
         
         mask = cv2.inRange(hsv, lower, upper)

         ys, xs = np.where(mask)

         if len(xs) == 0:
             continue
    
         centroid_x = left + xs.mean() 
         centroid_y = top + ys.mean()
         pygame.event.pump()

         
         if AXIS.get_axis(4) > 0.0:
             pt = ctypes.wintypes.POINT()
             ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
             grab_x, grab_y = pt.x, pt.y
    
             target_x = int(centroid_x)
             target_y = int(centroid_y)
    
             dx = target_x - grab_x 
             dy = target_y - grab_y -13

             dx = max(min(dx, 80), -80)
             dy = max(min(dy, 80), -80) 
             
             ctypes.windll.user32.mouse_event(0x0001, int(dx), int(dy))

      except Exception as err:
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)

def banner():
 os.system("cls")
 print(f"""                   
{h}         _ _            
   _____(_|_)   ______ _
  / ___/ / / | / / __ `/
 (__  ) / /| |/ / /_/ / 
/____/_/_/ |___/\__,_/                         
""")
 print(f"""{purple2}By LEVI &{h}& LONELY""")
 print(f"\033[0m\033[38;5;165m--UPDATE-\033[0mv\033[38;5;165m1")
 main()
banner()

