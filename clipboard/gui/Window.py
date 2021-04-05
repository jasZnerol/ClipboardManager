from tkinter import *
from functools import partial

from clipboard.gui.config import *
from clipboard.ClipboardManager import update_clipboard_data


class Window(object):
  def __init__(self, opts : dict = dict()):
    # State that will only change during runtime if you had a settings menu
    self.x_offset, self.y_offset = opts.get("position", default_values["position"]) # a tuple of the (x, y)-offset for the window.
    self.width, self.height = opts.get("size", default_values["size"]) # (width, height)
    self.transparency = opts.get("transparency", default_values["transparency"]) # value between 0 and 1
    self.hide_border = opts.get("hide_border", default_values["hide_border"])
    
    # For displaying the clipboard
    self.clipboard_font = ("Courier", 44)
    self.element_per_rows = self.height / 20
    self.element_per_columns =  self.width / 100

    # General gui stuff
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

    # Generate on click functions for each possible clibboard element displayed in the gui 
    def func(idx, event):
      update_clipboard_data(self.clipboard.goto(idx))
      self.update_clipboard()

    self.lable_on_click_functions = [partial(func, i) for i in range(100)]
  
  # Creates the tkinter instance. Can only be done because otherwise tkinter has problmens running in a thread
  # that we can manage ourselfs
  def run(self):
    self.root = Tk()
    self.root.withdraw()
    self.frame = Frame(self.root)
    self.update_window_properties()
    self.update_clipboard()
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
    # Clear the frame by destroying it and its children and create a new one
    for child in self.frame.winfo_children():
      child.pack_forget()
    self.frame.destroy()

    self.frame = Frame(self.root)
    for idx, elements  in enumerate(self.clipboard._memory):
      # Extract text
      lable_text = ""
      for typ, text in elements:
        if typ == 13: # plain text
          lable_text = text

      # Create lable for current element
      lable_text = lable_text if lable_text != "" else "No Plain Text"
      bg_color = "grey" if idx != self.clipboard._idx else "red"

      l = Label(self.frame, text=lable_text,  bg=bg_color)
      l.config(font=self.window.clipboard_font)
      l.grid(row=row, column=column, sticky=W, padx=10)
     
      l.bind("<Button-1>", self.lable_on_click_functions[idx])

      # Index stuff
      column += 1
      if (column == self.window.element_per_columns):
        row += 1
        column = 0
      if (row > self.window.element_per_rows):
        break

    self.frame.pack(padx=5, pady=10)
      

