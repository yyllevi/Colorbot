from mss import mss # by levi && lonely
import numpy as np
import ctypes
import pygame
import os
import time

os.system('cls')

left, top = 916, 400
width, height = 300, 300

pygame.init()
pygame.joystick.init()
AXIS = pygame.joystick.Joystick(0)
AXIS.init()

"""colors"""
red = "\033[1;31m"
purple2 = "\033[0;35m"
gray = "\033[1;30m"
dark_red = "\033[0;31m"
"""colors"""

def main():
 os.system("cls")
 print(f"""{gray}By LEVI && LONELY""")
 print(f"\033[0mactivate colorbot is on LT or RT, AIM BUTTON, UPDATE {gray}#4.5")

 with mss() as ss:
     while True:
         screen = {"left": left, "top": top, "width": width, "height": height}
         screenshot = np.array(ss.grab(screen))
    
         r, g, b = screenshot[:, :, 2], screenshot[:, :, 1], screenshot[:, :, 0]
         mask = (r >= 202) & (g <= 109 ) & (b >= 193)
         ys, xs = np.where(mask)
    
         if len(xs) == 0:
             time.sleep(0.001)
             continue
    
         centroid_x = xs.mean() 
         centroid_y = ys.min() + 18
    
         pygame.event.pump()
         if AXIS.get_axis(4) > 0.0:
             pt = ctypes.wintypes.POINT()
             ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
             grab_x, grab_y = pt.x, pt.y
    
             target_x = int(left + centroid_x)
             target_y = int(top + centroid_y)
    
             dx = target_x - grab_x 
             dy = target_y - grab_y 

             dx = max(min(dx, 50), -50)
             dy = max(min(dy, 50), -50) 
    
             ctypes.windll.user32.mouse_event(0x0001, dx, dy)
    
         time.sleep(0.001)

main()
