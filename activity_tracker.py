import time
import pyautogui
import keyboard
import math
import logging
import threading

# Parameters for flagging scripted activity
MOUSE_SPEED_THRESHOLD = 1000  # pixels/second
KEYBOARD_DELAY_THRESHOLD = 0.05  # seconds between key presses
MAX_EXECUTION_TIME = 60.0  # Maximum time to run the script in seconds

# Set up logging for flagged activities only
flagged_logger = logging.getLogger('flagged')
fh = logging.FileHandler('flagged_activity_log.txt')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
flagged_logger.addHandler(fh)

def track_mouse(max_time=MAX_EXECUTION_TIME):
    prev_x, prev_y = pyautogui.position()
    prev_time = time.time()
    start_time = time.time()
    
    while max_time is None or time.time() - start_time < max_time:
        curr_x, curr_y = pyautogui.position()
        curr_time = time.time()

        # Calculate distance moved
        distance = math.hypot(curr_x - prev_x, curr_y - prev_y)
        
        # Calculate time elapsed
        time_elapsed = curr_time - prev_time
        
        # Calculate speed (pixels/second)
        speed = distance / time_elapsed if time_elapsed > 0 else 0
        
        # Flag if speed is too consistent or too fast (indicating possible script)
        if speed > MOUSE_SPEED_THRESHOLD:
            flagged_logger.info("Flagged: Scripted mouse movement detected")
        
        # Update previous values
        prev_x, prev_y = curr_x, curr_y
        prev_time = curr_time
        
        # Sleep briefly to reduce CPU usage
        time.sleep(0.1)

def track_keyboard(max_time=MAX_EXECUTION_TIME):
    prev_time = time.time()
    start_time = time.time()
    
    def on_key_event(event):
        nonlocal prev_time
        curr_time = time.time()
        
        # Calculate time between key presses
        time_elapsed = curr_time - prev_time
        
        # Flag if delay is too short (indicating possible script)
        if time_elapsed < KEYBOARD_DELAY_THRESHOLD:
            flagged_logger.info(f"Flagged: Scripted keyboard input detected ({event.name})")
        
        # Update previous time
        prev_time = curr_time
    
    # Hook to monitor all key events
    keyboard.hook(on_key_event)
    
    # Keep the function running to monitor events
    try:
        while time.time() - float(start_time) < float(max_time):
            time.sleep(0.1)
        keyboard.unhook_all()  # Stop tracking after max_time
    except:
        pass

if __name__ == "__main__":
    # Run both tracking functions in parallel
    mouse_thread = threading.Thread(target=track_mouse)
    keyboard_thread = threading.Thread(target=track_keyboard)
    
    mouse_thread.start()
    keyboard_thread.start()
    
    mouse_thread.join()
    keyboard_thread.join()
    
    print("Activity monitoring completed.")
