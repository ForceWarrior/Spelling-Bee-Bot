import keyboard
import random
import time

def typeout(text):
    for char in text:
        keyboard.press_and_release(char)
        time.sleep(random.uniform(0.05, 0.125))
    keyboard.press_and_release('enter')