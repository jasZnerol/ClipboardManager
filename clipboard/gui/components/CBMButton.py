from tkinter import Button

from clipboard.gui.config import *

class CBMButton(Button):
  def __init__(self, frame, text, callback, bg=None, fg=None):
    bg = bg if bg != None else color_layers["layer1"]
    fg = fg if fg != None else color_layers["text"]
    super().__init__(frame, 
      text=text, 
      command=callback, 
      bg=bg, fg=fg, 
      activebackground=color_layers["layer2"], activeforeground=color_layers["text"]
    )
    self.bind("<Enter>", self.on_hovor_enter)
    self.bind("<Leave>", self.on_hovor_leave)

  def on_hovor_enter(self, event):
    self.configure(borderwidth=4)

  def on_hovor_leave(self, event):
    self.configure(borderwidth=2)
