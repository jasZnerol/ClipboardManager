# Screen dimensions
from win32api import GetSystemMetrics
import os
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

# Dict with a default value for every value
default_values = {
  "position": (int(screen_width  / 2 - (2/3 * screen_width)  / 2),  int(screen_height / 2 - (4/5 * screen_height) / 1.75)), # center
  "size": (int(2/3 * screen_width) , int(4/5 * screen_height)), # big
  "transparency": 0.9,
  "hide_border": False,
  "font": ("Courier", 20),
  "unknown_file_path": os.path.join(os.path.abspath("."), "resources", "unknown_file.png"),
  "image_size": (101, 128)
}

color_layers = {
  "background": "#10102D",
  "layer1": "#1A1131",
  "layer2": "#271235",
  "layer3": "#351339",
  "highlighted": "#3D1435",
  "text": "white"
}

# Return the width, length as a tuple for a given window size
# Will return None for invalid arg
def window_size(size: str):
  window_sizes = {
    "big": (int(2/3 * screen_width) , int(4/5 * screen_height)),
    "medium": (int(1/2 * screen_width) , int(1/2 * screen_height)),
    "small": (int(1/3 * screen_width) , int(1/4 * screen_height)),

    "default": (int(2/3 * screen_width) , int(4/5 * screen_height)),
  }
  return window_sizes.get(size)



# The ratios that 
"""
|-------------- Screen_top
|         I                 -> This marked length is how we add spacing from the top
|         V   Window_top    -> Therefore adding "screen_width / 2" will have the top line of our window at the middle of the screen
|     ##############        -> Therefore we want to subtract the half of our window size for the coordinates of our window to be centered
|     #
|-->  #                     (  This marked length is how we add spacing from the left  )
|     #                     
|     ############## 
|             Window_bottom
|
|-------------- Screen_bottom
"""
# Return the x/y offset for a window from left/top as a tuple for a given position name of a window
# Will return  None for invalid arg
def window_position(pos : str, window_width : int, window_height : int):
  # Stores the offset we need to add for (x_off, y_off) in order to position our window according to the name
  window_positions = {
    # Y-Achses is changing
    "top_center": (int(screen_width  / 2 - window_width  / 2), 0),
    "center":  (int(screen_width  / 2 - window_width  / 2),  int(screen_height / 2 - window_height / 2)),
    "bottom_center": (int(screen_width  / 2 - window_width  / 2),  screen_height - window_height),

    # Centered but y-achse wise a little elevated (look better). This is also the default
    "center_elevated":  (int(screen_width  / 2 - window_width  / 2),  int(screen_height / 2 - window_height / 1.75)),
    "default":  (int(screen_width  / 2 - window_width  / 2),  int(screen_height / 2 - window_height / 1.75)),

    # X-Achses is changing
    "center_left": (0, int(screen_height / 2 - window_height / 2)),
    "center_right": (screen_width - window_width, int(screen_height / 2 - window_height / 2)),

    # Corners
    "top_left": (0, 0),
    "top_right": (screen_width - window_width, 0),
    "bottom_left": (0, screen_height - window_height),
    "bottom_right": (screen_width - window_width, screen_height - window_height)
  }
  return window_positions.get(pos)


settings = {
  "text": ("type", "possible values"),
}