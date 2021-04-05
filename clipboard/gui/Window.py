from tkinter import *

from clipboard.gui.config import *




class Window(object):
  def __init__(self, opts : dict = dict()):
    self.x_offset, self.y_offset = opts.get("position", default_values["position"]) # a tuple of the (x, y)-offset for the window.
    self.width, self.height = opts.get("size", default_values["size"]) # (width, height)
    self.transparency = opts.get("transparency", default_values["transparency"]) # value between 0 and 1
    self.hide_border = opts.get("hide_border", default_values["hide_border"])
    self.visible = False

    self.element_rows = self.height / 20
    self.element_columns =  self.width / 100

  
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
    self.frame = Frame(self.root)
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
  def toggle_visibility(self):
    if self.window.visible:
      self.window.visible = False
      self.root.withdraw()
    else:
      self.window.visible = True
      self.root.deiconify()

  def shutdown(self):
    self.root.destroy()

  def update_clipboard(self):
    row, column = 0, 0
    
    for idx, elements  in enumerate(self.clipboard._memory):
      # Extract text
      lable_text = ""
      for typ, text in elements:
        if typ == 13: # plain text
          lable_text = text

      # Gui stuff
      l = Label(self.frame, text=lable_text if lable_text != "" else "No Plain Text",  bg="grey" if idx != self.clipboard._idx else "red")
      l.grid(row=row, column=column, sticky=W)

      # Index stuff
      column += 1
      if (column == self.window.element_columns):
        row += 1
        column = 0
      if (row > self.window.element_rows):
        break
    self.frame.pack(padx=5, pady=10)
      

    
