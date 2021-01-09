# This file allows you to determine the shortcuts you wish to associate with the eye
# movement. There are some predetermined functions below which can be copied and pasted
import pyautogui
import time


def handle_left(prev_cmd):
    if prev_cmd == 'L':
        pyautogui.hotkey('alt', 'tab')
    return 'L'


def handle_right(prev_cmd):
    if prev_cmd == 'R':
        roll_eyes()
    return 'R'


def handle_up(prev_cmd):
    if prev_cmd == 'U':
        pyautogui.write('sudo !!')
    return 'U'


def handle_down(prev_cmd):
    return 'D'


def handle_blink(count):
    if count == 2:
        pyautogui.hotkey('ctrl', 'shift', 'M')
    elif count == 3:
        im = pyautogui.screenshot()
        cfm = pyautogui.confirm('Save screenshot?')
        timeslot = time.time()
        if cfm == 'OK':
            im.save(f'./{timeslot}.png')
    elif count > 4:
        pyautogui.alert(text='We notice that you blinked a lot recently! Take a break.',
                        title='Tired eyes?', button='OK')
    return time.time()


def roll_eyes():
    print('''
    ___  ___          _              _____            ______      _ _           
    |  \/  |         | |            |  ___|           | ___ \    | | |          
    | .  . | __ _ ___| |_ ___ _ __  | |__ _   _  ___  | |_/ /___ | | | ___ _ __ 
    | |\/| |/ _` / __| __/ _ \ '__| |  __| | | |/ _ \ |    // _ \| | |/ _ \ '__|
    | |  | | (_| \__ \ ||  __/ |    | |__| |_| |  __/ | |\ \ (_) | | |  __/ |   
    \_|  |_/\__,_|___/\__\___|_|    \____/\__, |\___| \_| \_\___/|_|_|\___|_|   
                                           __/ |                                
                                          |___/                                 

    ''')
