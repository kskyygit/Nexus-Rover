import mss
import cv2
import numpy as np
import time
import pygetwindow as gw
import random
import pydirectinput
import ctypes
import os

pydirectinput.PAUSE = 0.1

try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

GAME_TITLE = "Poke Nexus"
FILE_FIGHT = "data/img/fight.jpg"
FILE_GRASS = "data/img/grass.jpg"
FILE_TURN = "data/img/turn.jpg"
FOLDER_MAPS = "data/maps"

CONFIDENCE_FIGHT = 0.8
CONFIDENCE_GRASS = 0.15
CONFIDENCE_MAP = 0.85
SCAN_DIST = 110

def get_screen(window):
    with mss.mss() as sct:
        monitor = {"top": int(window.top), "left": int(window.left), "width": int(window.width), "height": int(window.height)}
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def find_image(screen, path, confidence):
    template = cv2.imread(path)
    if template is None: return False, None
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > confidence:
        h, w = template.shape[:2]
        return True, (max_loc[0] + w//2, max_loc[1] + h//2)
    return False, None

def hard_reset_keys():
   
    for key in ['w', 'a', 's', 'd', '1', '2', '3', '4', 'space', 'shift', 'enter']:
        pydirectinput.keyUp(key)

def execute_city_path(file_name):
    city_display_name = file_name.split('.')[0].capitalize()
    name = file_name.lower()
    
    print(f"[CITY DETECTED] Navigating through: {city_display_name}")
    
    hard_reset_keys() 
    if "celadon" in name:
        pydirectinput.keyDown('s'); time.sleep(2.5); pydirectinput.keyUp('s'); time.sleep(0.2)
        pydirectinput.keyDown('d'); time.sleep(13.0); pydirectinput.keyUp('d'); time.sleep(0.2)
        pydirectinput.keyDown('w'); time.sleep(3.0); pydirectinput.keyUp('w')
    elif "cerulean" in name:
        pydirectinput.keyDown('s'); time.sleep(2.8); pydirectinput.keyUp('s'); time.sleep(0.5)
        pydirectinput.keyDown('a'); time.sleep(5.5); pydirectinput.keyUp('a'); time.sleep(0.5)
        pydirectinput.keyDown('w'); time.sleep(4.0); pydirectinput.keyUp('w'); time.sleep(0.5)
        pydirectinput.keyDown('a'); time.sleep(8.5); pydirectinput.keyUp('a'); time.sleep(0.5)
        pydirectinput.keyDown('s'); time.sleep(3.5); pydirectinput.keyUp('s'); time.sleep(0.5)
        pydirectinput.keyDown('a'); time.sleep(4.5); pydirectinput.keyUp('a'); time.sleep(0.5)
    
    hard_reset_keys()
    print(f"[PATH] {city_display_name} navigation finished.")

windows = gw.getWindowsWithTitle(GAME_TITLE)
if not windows:
    print("[ERROR] Window not found!"); exit()
win = windows[0]
win.activate()
time.sleep(2)

while True:
    try:
        frame = get_screen(win)
    except: continue

    if os.path.exists(FOLDER_MAPS):
        detected_city = None
        for file in os.listdir(FOLDER_MAPS):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                if find_image(frame, os.path.join(FOLDER_MAPS, file), CONFIDENCE_MAP)[0]:
                    detected_city = file
                    break
        if detected_city:
            execute_city_path(detected_city)
            continue

    battle, _ = find_image(frame, FILE_FIGHT, CONFIDENCE_FIGHT)
    if not battle:
        battle, _ = find_image(frame, FILE_TURN, CONFIDENCE_FIGHT)

    if battle:
        print("[BATTLE] Turn detected! Emergency Reset & Attack...")
        hard_reset_keys()
        
        time.sleep(0.8) 
        
        pydirectinput.keyDown('1')
        time.sleep(0.15)
        pydirectinput.keyUp('1')
        time.sleep(0.3)
        pydirectinput.keyDown('1')
        time.sleep(0.15)
        pydirectinput.keyUp('1')

        time.sleep(2.0) 

        random.seed()
        atk = random.choice(['1', '2', '3', '4'])
        print(f"[BATTLE] Phase 2: Sending attack {atk}")
        
        pydirectinput.keyDown(atk)
        time.sleep(0.15)
        pydirectinput.keyUp(atk)

        time.sleep(4.0)
        continue

    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    move_list = ['w', 's', 'a', 'd']
    random.shuffle(move_list)

    for direction in move_list:
        offsets = {'w': (0, -SCAN_DIST), 's': (0, SCAN_DIST), 'a': (-SCAN_DIST, 0), 'd': (SCAN_DIST, 0)}
        tx, ty = center_x + offsets[direction][0], center_y + offsets[direction][1]
        x1, y1 = max(0, int(tx-60)), max(0, int(ty-60))
        x2, y2 = min(width, int(tx+60)), min(height, int(ty+60))
        
        if find_image(frame[y1:y2, x1:x2], FILE_GRASS, CONFIDENCE_GRASS)[0]:
            pydirectinput.keyDown(direction); time.sleep(0.4); pydirectinput.keyUp(direction)
            break
    
    time.sleep(0.1)