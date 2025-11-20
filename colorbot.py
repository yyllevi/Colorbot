from mss import mss  # by levi && lonely
import numpy as np
import ctypes
from ctypes import wintypes
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

    # ---- init pygame & controller ONCE ----
    pygame.init()
    pygame.joystick.init()
    try:
        AXIS = pygame.joystick.Joystick(0)
        AXIS.init()
    except Exception:
        print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
        time.sleep(3)
        return

    moves_mouse = 0x0001

    with mss() as ss:
        while True:
            try:
                screen = {"left": left, "top": top, "width": width, "height": height}
                screenshot = np.array(ss.grab(screen))

                # split channels (BGR from MSS)
                r, g, b = screenshot[:, :, 2], screenshot[:, :, 1], screenshot[:, :, 0]

                # your purple mask
                mask = (r >= 190) & (g <= 109) & (b >= 192)
                ys, xs = np.where(mask)

                pygame.event.pump()
                lt_pressed = AXIS.get_axis(4) > 0.0

                if not lt_pressed:
                    continue  # nothing if LT not held

                # ---------- NO COLOR: jitter ----------
                if len(xs) == 0:
                    move_left = -25 
                    move_right = -25 
                    move_down = 25
                    move_up = 25

                    ctypes.windll.user32.mouse_event(moves_mouse,move_up,move_right) 
                    time.sleep(0.0088)
                    ctypes.windll.user32.mouse_event(moves_mouse,move_left,move_down)
                    time.sleep(0.0088)
                    continue

                # ---------- COLOR FOUND: lock on ----------
                centroid_x = left + xs.mean()
                centroid_y = top + ys.mean()

                pt = wintypes.POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
                grab_x, grab_y = pt.x, pt.y

                target_x = int(centroid_x)
                target_y = int(centroid_y)

                dx = target_x - grab_x
                dy = target_y - grab_y - 18  # little offset

                # clamp to stop spazzing
                dx = max(min(dx, 80), -80)
                dy = max(min(dy, 80), -80)

                ctypes.windll.user32.mouse_event(moves_mouse, int(dx), int(dy))

            except Exception as err:
                print(f"{red}PLEASE PLUG IN YOUR CONTROLLER! ({err})")
                time.sleep(1.5)


if __name__ == "__main__":
    main()
