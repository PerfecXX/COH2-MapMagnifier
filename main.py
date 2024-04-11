"""
Author: Teeraphat Kullanankanjana
version: 0.1
Date: 12/04/2024
Description: Map Magnifier for Company of Hero 2
Copyright (C) 2024 Teeraphat Kullanankanjana. All right reserved.
"""

# Import Library
import cv2
import numpy as np
from pyautogui import screenshot
from tkinter import *
from PIL import Image, ImageTk

# Function to capture game window and resize it to fit GUI
def capture_game_window():
    # Capture screenshot of the game window
    game_window = screenshot(region=(game_window_x, game_window_y, game_window_width, game_window_height))
    # Convert screenshot to OpenCV format (BGR)
    game_frame = cv2.cvtColor(np.array(game_window), cv2.COLOR_RGB2BGR)
    # Crop to the map area
    map_area = game_frame[map_area_y:map_area_y + map_area_height, map_area_x:map_area_x + map_area_width]
    # Resize to fit the GUI
    resized_frame = cv2.resize(map_area, (output_width, output_height))
    # Convert BGR to RGB format
    return cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

# Function to update displayed image
def update_image():
    # Check if the root window still exists
    if root.winfo_exists():
        # Capture the game window and update the displayed image
        game_frame = capture_game_window()
        img = Image.fromarray(game_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label_img.imgtk = imgtk
        label_img.configure(image=imgtk)
        # Schedule the next update after 10 milliseconds
        label_img.after(10, update_image)

# Read settings from text file
def read_settings(filename):
    settings = {}
    with open(filename, 'r') as file:
        # Read each line in the settings file
        for line in file:
            # Split the line into key and value pairs
            key, value = line.strip().split(':')
            # Store the key-value pair in the settings dictionary after stripping whitespace
            settings[key.strip()] = int(value.strip())
    return settings

# Read settings from file
settings = read_settings("settings.txt")

# Game window parameters
game_window_x = settings['game_window_x']              # X coordinate of top-left corner of game window
game_window_y = settings['game_window_y']              # Y coordinate of top-left corner of game window
game_window_width = settings['game_window_width']      # Width of the game window
game_window_height = settings['game_window_height']    # Height of the game window

# Map area parameters
map_area_x = settings['map_area_x']                    # X coordinate of top-left corner of map area
map_area_y = settings['map_area_y']                    # Y coordinate of top-left corner of map area
map_area_width = settings['map_area_width']            # Width of the map area
map_area_height = settings['map_area_height']          # Height of the map area

# Output window size
output_width = settings['output_width']                # Width of the output window
output_height = settings['output_height']              # Height of the output window

# Create Tkinter window
root = Tk()
root.title("COH2 Map Magnifier")
root.geometry(f"{output_width}x{output_height}")

# Create label for displaying captured image
label_img = Label(root)
label_img.pack()

# Start capturing and updating image
update_image()

# Run the Tkinter event loop
root.mainloop()

