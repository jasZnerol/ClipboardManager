from tkinter import *

try:
  from clipboard.gui.config import *
except:
  from config import *



class Window(object):
  def __init__(self, opts : dict = dict()):
    self.x_offset, self.y_offset = opts.get("position", default_values["position"]) # a tuple of the (x, y)-offset for the window.
    self.width, self.height = opts.get("size", default_values["size"]) # (width, height)
    self.transparency = opts.get("transparency", default_values["transparency"]) # value between 0 and 1
    self.hide_border = opts.get("hide_border", default_values["hide_border"])
    self.visible = False
  
  # Update with a given opts-dictionary. If a key is not found don't change the window configuration in that aspect
  def update(self, opts):
    self.x_offset, self.y_offset = opts.get("position", (self.x_offset, self.y_offset))
    self.width, self.height = opts.get("size", ( self.width, self.height))
    self.transparency = opts.get("transparency", self.transparency) 
    self.hide_border = opts.get("hide_border", self.hide_border)

class CBMWindow(object):
  def __init__(self, clipboard):
    self.clipboard = clipboard
    self.window = Window()
  
  # Creates the tkinter instance. Can only be done because otherwise tkinter has problmens running in a thread
  # that we can manage ourselfs
  def run(self):
    self.root = Tk()
    self.root.withdraw()
    self.update_window_properties()
    self.root.mainloop()
  
  # Applys all properties set in self.window to the tkinter window
  def update_window_properties(self):
    # Update size and position
    self.root.geometry("{0}x{1}+{2}+{3}".format(self.window.width, self.window.height, self.window.x_offset, self.window.y_offset)) 
    # Set generall transparency
    self.root.attributes('-alpha', self.window.transparency)
    # En/Disable border
    self.root.overrideredirect(1 if self.window.hide_border else 0) # Remove border


  # Interface functions for keyboard controll
  def change_visibility(self):
    if self.window.visible:
      self.window.visible = False
      self.root.withdraw()
    else:
      self.window.visible = True
      self.root.deiconify()

  def shutdown(self):
    self.root.destroy()

  def update_clipboard(self):
    pass
