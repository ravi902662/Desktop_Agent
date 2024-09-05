# # import tkinter as tk
# # import threading
# # import time
# # from datetime import datetime
# # from PIL import Image, ImageFilter
# # import pytz
# # from zoneinfo import ZoneInfo  # For Python 3.9+
# # import screenshot_capture
# # import activity_tracker
# # import logging

# # class ActivityApp:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Activity Tracker and Screenshot Capture")

# #         # GUI Configuration
# #         self.label = tk.Label(root, text="Monitoring in background...")
# #         self.label.pack(pady=10)

# #         # Initialize settings
# #         self.current_timezone = self.get_local_timezone()
# #         self.screenshot_interval = 60  # Default interval
# #         self.capture_screenshots = True
# #         self.blur_screenshots = False
        
# #         # Set up logging
# #         self.setup_logging()

# #         # Create stop event
# #         self.stop_event = threading.Event()

# #         # Start monitoring, screenshot capture, and timezone check in background
# #         self.start_monitoring()

# #         # Add settings button
# #         settings_button = tk.Button(root, text="Settings", command=self.open_settings_window)
# #         settings_button.pack(pady=10)

# #     def get_local_timezone(self):
# #         # For Python 3.9+, use ZoneInfo to get local timezone
# #         local_timezone = datetime.now().astimezone().tzinfo
# #         return local_timezone

# #     def setup_logging(self):
# #         # Configure logging
# #         logging.basicConfig(
# #             filename='activity_log.txt',
# #             level=logging.INFO,
# #             format='%(asctime)s - %(levelname)s - %(message)s'
# #         )
# #         logging.info("Activity logging started.")

# #     def start_monitoring(self):
# #         # Start activity tracking and screenshot capture in separate threads
# #         self.tracking_thread = threading.Thread(target=self.run_tracking)
# #         self.screenshot_thread = threading.Thread(target=self.capture_screenshot_periodically)
# #         self.timezone_thread = threading.Thread(target=self.check_timezone_changes)

# #         self.tracking_thread.start()
# #         self.screenshot_thread.start()
# #         self.timezone_thread.start()

# #     def run_tracking(self):
# #         # Run both tracking functions
# #         mouse_thread = threading.Thread(target=self.track_mouse)
# #         keyboard_thread = threading.Thread(target=self.track_keyboard)

# #         mouse_thread.start()
# #         keyboard_thread.start()

# #         mouse_thread.join()
# #         keyboard_thread.join()

# #     def track_mouse(self):
# #         activity_tracker.track_mouse(max_time=None)  # No max_time since it's controlled by stop_event

# #     def track_keyboard(self):
# #         activity_tracker.track_keyboard(max_time=None)  # No max_time since it's controlled by stop_event

# #     def capture_screenshot_periodically(self):
# #         while not self.stop_event.is_set():
# #             if self.capture_screenshots:
# #                 screenshot = screenshot_capture.capture_screenshot()
# #                 if self.blur_screenshots:
# #                     screenshot = screenshot.filter(ImageFilter.GaussianBlur(radius=5))
# #                 # screenshot.save('screenshot.png')
# #                 # self.upload_to_s3('screenshot.png')
# #             time.sleep(self.screenshot_interval)

# #     def check_timezone_changes(self):
# #         while not self.stop_event.is_set():
# #             new_timezone = self.get_local_timezone()
# #             if new_timezone != self.current_timezone:
# #                 self.current_timezone = new_timezone
# #                 self.handle_timezone_change()
# #             time.sleep(60)  # Check for time zone changes every 60 seconds

# #     def handle_timezone_change(self):
# #         # Handle the time zone change
# #         timezone_message = f"Time zone changed to {self.current_timezone}"
# #         logging.info(timezone_message)
# #         print(timezone_message)

# #     def open_settings_window(self):
# #         settings_window = tk.Toplevel(self.root)
# #         settings_window.title("Settings")
        
# #         # Screenshot Interval
# #         interval_label = tk.Label(settings_window, text="Screenshot Interval (seconds):")
# #         interval_label.pack()
# #         self.interval_entry = tk.Entry(settings_window)
# #         self.interval_entry.insert(0, str(self.screenshot_interval))
# #         self.interval_entry.pack()
        
# #         # Screenshot Capture Toggle
# #         capture_var = tk.BooleanVar(value=self.capture_screenshots)
# #         capture_checkbox = tk.Checkbutton(settings_window, text="Capture Screenshots", variable=capture_var)
# #         capture_checkbox.pack()
        
# #         # Blur Screenshot Toggle
# #         blur_var = tk.BooleanVar(value=self.blur_screenshots)
# #         blur_checkbox = tk.Checkbutton(settings_window, text="Blur Screenshots", variable=blur_var)
# #         blur_checkbox.pack()
        
# #         # Save Button
# #         save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(capture_var.get(), blur_var.get()))
# #         save_button.pack()

# #     def save_settings(self, capture_screenshots, blur_screenshots):
# #         try:
# #             self.screenshot_interval = int(self.interval_entry.get())
# #         except ValueError:
# #             print("Invalid interval. Using default.")
# #             self.screenshot_interval = 60
# #         self.capture_screenshots = capture_screenshots
# #         self.blur_screenshots = blur_screenshots

# #     def stop(self):
# #         self.stop_event.set()  # Signal threads to stop
# #         self.tracking_thread.join()
# #         self.screenshot_thread.join()
# #         self.timezone_thread.join()
# #         logging.info("Monitoring stopped.")

# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = ActivityApp(root)
    
# #     try:
# #         root.mainloop()
# #     except KeyboardInterrupt:
# #         app.stop()
# #         print("Monitoring stopped.")
# import tkinter as tk
# from tkinter import ttk
# import threading
# import time
# from datetime import datetime
# from PIL import Image, ImageFilter
# import pytz
# from zoneinfo import ZoneInfo  # For Python 3.9+
# import screenshot_capture
# import activity_tracker
# import logging

# class ActivityApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Activity Tracker and Screenshot Capture")

#         # Set window size and position
#         self.root.geometry("400x300")
#         self.root.resizable(False, False)

#         # Set styles
#         self.style = ttk.Style()
#         self.style.configure("TButton", font=("Helvetica", 12), padding=6)
#         self.style.configure("TLabel", font=("Helvetica", 12))
#         self.style.configure("TFrame", background="#f0f0f0")
#         self.style.configure("TCheckbutton", font=("Helvetica", 11))

#         # Main Frame
#         self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
#         self.main_frame.pack(expand=True, fill=tk.BOTH)

#         # Header Label
#         self.label = ttk.Label(self.main_frame, text="Monitoring in background...")
#         self.label.pack(pady=20)

#         # Add settings button
#         settings_button = ttk.Button(self.main_frame, text="Settings", command=self.open_settings_window)
#         settings_button.pack(pady=10)

#         # Initialize settings
#         self.current_timezone = self.get_local_timezone()
#         self.screenshot_interval = 60  # Default interval
#         self.capture_screenshots = True
#         self.blur_screenshots = False
        
#         # Set up logging
#         self.setup_logging()

#         # Create stop event
#         self.stop_event = threading.Event()

#         # Start monitoring, screenshot capture, and timezone check in background
#         self.start_monitoring()

#     def get_local_timezone(self):
#         # For Python 3.9+, use ZoneInfo to get local timezone
#         local_timezone = datetime.now().astimezone().tzinfo
#         return local_timezone

#     def setup_logging(self):
#         # Configure logging
#         logging.basicConfig(
#             filename='activity_log.txt',
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s - %(message)s'
#         )
#         logging.info("Activity logging started.")

#     def start_monitoring(self):
#         # Start activity tracking and screenshot capture in separate threads
#         self.tracking_thread = threading.Thread(target=self.run_tracking)
#         self.screenshot_thread = threading.Thread(target=self.capture_screenshot_periodically)
#         self.timezone_thread = threading.Thread(target=self.check_timezone_changes)

#         self.tracking_thread.start()
#         self.screenshot_thread.start()
#         self.timezone_thread.start()

#     def run_tracking(self):
#         # Run both tracking functions
#         mouse_thread = threading.Thread(target=self.track_mouse)
#         keyboard_thread = threading.Thread(target=self.track_keyboard)

#         mouse_thread.start()
#         keyboard_thread.start()

#         mouse_thread.join()
#         keyboard_thread.join()

#     def track_mouse(self):
#         activity_tracker.track_mouse(max_time=None)  # No max_time since it's controlled by stop_event

#     def track_keyboard(self):
#         activity_tracker.track_keyboard(max_time=None)  # No max_time since it's controlled by stop_event

#     def capture_screenshot_periodically(self):
#         while not self.stop_event.is_set():
#             if self.capture_screenshots:
#                 screenshot = screenshot_capture.capture_screenshot()
#                 if self.blur_screenshots:
#                     screenshot = screenshot.filter(ImageFilter.GaussianBlur(radius=5))
#                 # screenshot.save('screenshot.png')
#                 # self.upload_to_s3('screenshot.png')
#             time.sleep(self.screenshot_interval)

#     def check_timezone_changes(self):
#         while not self.stop_event.is_set():
#             new_timezone = self.get_local_timezone()
#             if new_timezone != self.current_timezone:
#                 self.current_timezone = new_timezone
#                 self.handle_timezone_change()
#             time.sleep(60)  # Check for time zone changes every 60 seconds

#     def handle_timezone_change(self):
#         # Handle the time zone change
#         timezone_message = f"Time zone changed to {self.current_timezone}"
#         logging.info(timezone_message)
#         print(timezone_message)

#     def open_settings_window(self):
#         settings_window = tk.Toplevel(self.root)
#         settings_window.title("Settings")
#         settings_window.geometry("300x250")
#         settings_window.resizable(False, False)
        
#         # Frame for settings
#         settings_frame = ttk.Frame(settings_window, padding="10 10 10 10")
#         settings_frame.pack(expand=True, fill=tk.BOTH)

#         # Screenshot Interval
#         interval_label = ttk.Label(settings_frame, text="Screenshot Interval (seconds):")
#         interval_label.pack(pady=(10, 5))
#         self.interval_entry = ttk.Entry(settings_frame)
#         self.interval_entry.insert(0, str(self.screenshot_interval))
#         self.interval_entry.pack(pady=(0, 10))
        
#         # Screenshot Capture Toggle
#         capture_var = tk.BooleanVar(value=self.capture_screenshots)
#         capture_checkbox = ttk.Checkbutton(settings_frame, text="Capture Screenshots", variable=capture_var)
#         capture_checkbox.pack(pady=(5, 10))
        
#         # Blur Screenshot Toggle
#         blur_var = tk.BooleanVar(value=self.blur_screenshots)
#         blur_checkbox = ttk.Checkbutton(settings_frame, text="Blur Screenshots", variable=blur_var)
#         blur_checkbox.pack(pady=(5, 20))
        
#         # Save Button
#         save_button = ttk.Button(settings_frame, text="Save", command=lambda: self.save_settings(capture_var.get(), blur_var.get()))
#         save_button.pack()

#     def save_settings(self, capture_screenshots, blur_screenshots):
#         try:
#             self.screenshot_interval = int(self.interval_entry.get())
#         except ValueError:
#             print("Invalid interval. Using default.")
#             self.screenshot_interval = 60
#         self.capture_screenshots = capture_screenshots
#         self.blur_screenshots = blur_screenshots

#     def stop(self):
#         self.stop_event.set()  # Signal threads to stop
#         self.tracking_thread.join()
#         self.screenshot_thread.join()
#         self.timezone_thread.join()
#         logging.info("Monitoring stopped.")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ActivityApp(root)
    
#     try:
#         root.mainloop()
#     except KeyboardInterrupt:
#         app.stop()
#         print("Monitoring stopped.")
import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
from PIL import Image, ImageFilter
import pytz
from zoneinfo import ZoneInfo  # For Python 3.9+
import screenshot_capture
import activity_tracker
import logging

class ActivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Tracker and Screenshot Capture")

        # Set window size and position
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Set styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TCheckbutton", font=("Helvetica", 11))

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Header Label
        self.label = ttk.Label(self.main_frame, text="Monitoring in background...")
        self.label.pack(pady=20)

        # Add settings button
        settings_button = ttk.Button(self.main_frame, text="Settings", command=self.open_settings_window)
        settings_button.pack(pady=10)

        # Initialize settings
        self.current_timezone = self.get_local_timezone()
        self.screenshot_interval = 60  # Default interval
        self.capture_screenshots = True
        self.blur_screenshots = False
        
        # Set up logging
        self.setup_logging()

        # Create stop event
        self.stop_event = threading.Event()

        # Start monitoring, screenshot capture, and timezone check in background
        self.start_monitoring()

    def get_local_timezone(self):
        # For Python 3.9+, use ZoneInfo to get local timezone
        local_timezone = datetime.now().astimezone().tzinfo
        return local_timezone

    def setup_logging(self):
        # Configure logging
        logging.basicConfig(
            filename='activity_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Activity logging started.")

    def start_monitoring(self):
        # Start activity tracking and screenshot capture in separate threads
        self.tracking_thread = threading.Thread(target=self.run_tracking)
        self.screenshot_thread = threading.Thread(target=self.capture_screenshot_periodically)
        self.timezone_thread = threading.Thread(target=self.check_timezone_changes)

        self.tracking_thread.start()
        self.screenshot_thread.start()
        self.timezone_thread.start()

    def stop_monitoring(self):
        self.stop_event.set()  # Signal threads to stop
        self.tracking_thread.join()
        self.screenshot_thread.join()
        self.timezone_thread.join()
        self.stop_event.clear()  # Clear stop event for restarting

    def run_tracking(self):
        # Run both tracking functions
        mouse_thread = threading.Thread(target=self.track_mouse)
        keyboard_thread = threading.Thread(target=self.track_keyboard)

        mouse_thread.start()
        keyboard_thread.start()

        mouse_thread.join()
        keyboard_thread.join()

    def track_mouse(self):
        activity_tracker.track_mouse(max_time=None)  # No max_time since it's controlled by stop_event

    def track_keyboard(self):
        activity_tracker.track_keyboard(max_time=None)  # No max_time since it's controlled by stop_event

    def capture_screenshot_periodically(self):
        while not self.stop_event.is_set():
            if self.capture_screenshots:
                screenshot = screenshot_capture.capture_screenshot()
                if self.blur_screenshots:
                    screenshot = screenshot.filter(ImageFilter.GaussianBlur(radius=5))
                # screenshot.save('screenshot.png')
                # self.upload_to_s3('screenshot.png')
            time.sleep(self.screenshot_interval)

    def check_timezone_changes(self):
        while not self.stop_event.is_set():
            new_timezone = self.get_local_timezone()
            if new_timezone != self.current_timezone:
                self.current_timezone = new_timezone
                self.handle_timezone_change()
            time.sleep(60)  # Check for time zone changes every 60 seconds

    def handle_timezone_change(self):
        # Handle the time zone change
        timezone_message = f"Time zone changed to {self.current_timezone}"
        logging.info(timezone_message)
        print(timezone_message)

    def open_settings_window(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x250")
        settings_window.resizable(False, False)
        
        # Frame for settings
        settings_frame = ttk.Frame(settings_window, padding="10 10 10 10")
        settings_frame.pack(expand=True, fill=tk.BOTH)

        # Screenshot Interval
        interval_label = ttk.Label(settings_frame, text="Screenshot Interval (seconds):")
        interval_label.pack(pady=(10, 5))
        self.interval_entry = ttk.Entry(settings_frame)
        self.interval_entry.insert(0, str(self.screenshot_interval))
        self.interval_entry.pack(pady=(0, 10))
        
        # Screenshot Capture Toggle
        self.capture_var = tk.BooleanVar(value=self.capture_screenshots)
        capture_checkbox = ttk.Checkbutton(settings_frame, text="Capture Screenshots", variable=self.capture_var)
        capture_checkbox.pack(pady=(5, 10))
        
        # Blur Screenshot Toggle
        self.blur_var = tk.BooleanVar(value=self.blur_screenshots)
        blur_checkbox = ttk.Checkbutton(settings_frame, text="Blur Screenshots", variable=self.blur_var)
        blur_checkbox.pack(pady=(5, 20))
        
        # Save Button
        save_button = ttk.Button(settings_frame, text="Save", command=lambda: self.save_settings(settings_window))
        save_button.pack()

    def save_settings(self, settings_window):
        try:
            self.screenshot_interval = int(self.interval_entry.get())
        except ValueError:
            print("Invalid interval. Using default.")
            self.screenshot_interval = 60
        self.capture_screenshots = self.capture_var.get()
        self.blur_screenshots = self.blur_var.get()

        # Restart monitoring with the new settings
        self.stop_monitoring()
        self.start_monitoring()

        # Close the settings window
        settings_window.destroy()

    def stop(self):
        self.stop_event.set()  # Signal threads to stop
        self.tracking_thread.join()
        self.screenshot_thread.join()
        self.timezone_thread.join()
        logging.info("Monitoring stopped.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.stop()
        print("Monitoring stopped.")
