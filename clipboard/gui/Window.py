from tkinter import *
from tkinter import ttk
from functools import partial

from clipboard.gui.config import *
from clipboard.ClipboardManager import update_clipboard_data
from PIL import ImageTk, Image

class Window(object):
  def __init__(self, opts : dict = dict()):
    # State that will only change during runtime if you had a settings menu
    self.x_offset, self.y_offset = opts.get("position", default_values["position"]) # a tuple of the (x, y)-offset for the window.
    self.width, self.height = opts.get("size", default_values["size"]) # (width, height)
    self.transparency = opts.get("transparency", default_values["transparency"]) # value between 0 and 1
    self.hide_border = opts.get("hide_border", default_values["hide_border"])
    
    # For displaying the clipboard
    self.font = opts.get("font", default_values["font"])
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

    self.images = dict()

    # Generate on click functions for each possible clibboard element displayed in the gui 
    def func(idx, event):
      update_clipboard_data(self.clipboard.goto(idx))
      self.update_clipboard()

    self.lable_on_click_functions = [partial(func, i) for i in range(100)]

  
  def create_header(self):
    def clear():
      self.clipboard.clear()
      self.update_clipboard()
    def open_webpage():
      import webbrowser
      from clipboard.config import webpage
      webbrowser.open(webpage)

    # Dictionary for header buttons
    self.header_buttons = {
      "Webpage": open_webpage,
      "Clear":  clear,
      "Settings": self.open_settings,
      "Quit":  self.shutdown
    }

    self.header = Frame(self.root)	
    # Setup header
    i = 0
    for text, func in self.header_buttons.items():
      b = Button(self.header, text=text, command=func)
      b.config(font=self.window.font)
      b.grid(row=0, column=i, sticky=W, padx=10, pady=10)
      i += 1

    # Create seperator between header and clipboard stuff
    s = ttk.Separator(self.header, orient='horizontal')
    s.place(relx=0, rely=0.99, relwidth=1, relheight=1)

    self.header.pack(pady=20)

  # Creates the tkinter instance. Can only be done because otherwise tkinter has problmens running in a thread
  # that we can manage ourselfs
  def run(self):
    self.root = Tk()
    self.root.withdraw()
    self.frame = Frame(self.root)

    self.create_header()

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
    self.window.visible = "normal" == self.root.state()
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
      is_image = False
      for typ, text in elements:
        if typ == 13: # plain text
          lable_text = text
          break
        # TODO: Optimize this: This now loads the image and resizes it every time
        #       Also this only works for a local machine. We will need to check if the image
        #       Can be found on this machine and if not REQUEST it from the server
        if typ == 15: #image
          # Get image and store variable as to not lose it
          lable_text = text[0]
          image = ImageTk.PhotoImage(Image.open(lable_text).resize((128, 128), Image.ANTIALIAS))
          self.images[lable_text] = image
          is_image = True
          break

      # Set bg color depending on if element is selected or not
      bg_color = "grey" if idx != self.clipboard._idx else "red"
      # Select an image if the current element is an image
      image = self.images[lable_text] if is_image else None

      # Create lable for current element
      l = Label(self.frame, text=lable_text, image=image, bg=bg_color)
      l.config(font=self.window.font)
      l.grid(row=row, column=column, sticky=W, padx=10)
      l.bind("<Button-1>", self.lable_on_click_functions[idx])

      # Index stuff
      column += 1
      if (column == self.window.element_per_columns):
        row += 1
        column = 0
      if (row > self.window.element_per_rows):
        break
      self.frame.pack()
      
  def open_settings(self):
    self.settings = Toplevel(self.root)
    self.settings.title("Settings")
    self.settings.geometry("{0}x{1}+{2}+{3}".format(
      int(self.window.width / 2), 
      int(self.window.height / 2), 
      self.window.x_offset * 2, 
      self.window.y_offset * 3)
    ) 

