from bettercam import create  # by levi && lonely
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
    print(f"\033[0m{red}UPDATE {gray}#using bettercam cause mss way slower")

    # ---- BetterCam setup ----
    # bettercam expects (left, top, right, bottom)
    region = (left, top, left + width, top + height)

    cam = create(
        output_idx=0,          # main monitor
        region=region
    )
    # optional but good: start capture thread
    try:
        cam.start(target_fps=240)
    except Exception:
        # some versions autostart on first grab, so ignore if not supported
        pass

    # init pygame once, not every frame
    pygame.init()
    pygame.joystick.init()
    AXIS = pygame.joystick.Joystick(0)
    AXIS.init()

    while True:
        try:
            # Grab region with bettercam (BGR numpy array)
            screenshot = cam.get_latest_frame()

            if screenshot is None:
                continue

            r, g, b = screenshot[:, :, 2], screenshot[:, :, 1], screenshot[:, :, 0]
            mask = (r >= 190) & (g <= 109) & (b >= 192)
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
                dy = target_y - grab_y - 18

                dx = max(min(dx, 80), -80)
                dy = max(min(dy, 80), -80)

                ctypes.windll.user32.mouse_event(0x0001, dx, dy)

        except Exception:
            print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
            time.sleep(1.5)
            print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
            time.sleep(1.5)
            print(f"{red}PLEASE PLUG IN YOUR CONTROLLER!")
            time.sleep(1.5)


main()
