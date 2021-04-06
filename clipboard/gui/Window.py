from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import ImageTk, Image

from clipboard.gui.config import *
from clipboard.ClipboardManager import update_clipboard_data
from utils.img import merge_images


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
    self.root.title("CBMWindow")
    self.frame = Frame(self.root)

    self.create_header()

    # Cannot be done in init as root has to exists first
    self.images = {
      "unknown_file_image":   ImageTk.PhotoImage(
            Image.open(default_values["unknown_file_path"]).resize(default_values["image_size"], Image.ANTIALIAS)
        )
    }


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
  # TODO: Stop windows bar notifications
  def toggle_visibility(self):
    if self.window.visible:
      self.window.visible = False
      self.root.withdraw()
    else:
      self.root.attributes("-topmost", True) # Overlay
      self.window.visible = True
      self.root.deiconify()

  def shutdown(self):
    self.root.destroy()



  # TODO: simplify/minimize this function:
  #       It should simply update the image cache according to the data stored in the clipboard (single files, string, file-lists etc.)
  def update_images(self):
    # Remove images that have been removed from clipboard in the mean-time
    to_remove = []
    for image in self.images:
      # Skip default image
      if image == "unknown_file_image":
        continue
      found = False
      # check if any clipboard "element" (which itself can be a list) contains an image we no longer require
      # if an image from the images stored is not in the clipboard we can remove it from the clipboard list
      for ele in self.clipboard._memory:
        for typ, data in ele:
          if typ == 15:
            total_key = ""
            # Check for single images
            for file in data:
              total_key += file	
              if file == image:
                found = True
              # Check if all file paths as one string are a key vor a list-image
              if total_key == image:
                found = True
          if found:
            break
        if found:
          break
      if not found:
        to_remove.append(image)
      found = False
    for remove in to_remove:
      del self.images[remove]
    
    # Add new images found in the clipboard
    for ele in self.clipboard._memory:
      for typ, data in ele:
        if typ == 15: # file type
          total_key = ""
          image_list = []	
          for file in data:
            try: 
              total_key += file
              if file not in self.images:
                image = ImageTk.PhotoImage(Image.open(file).resize(default_values["image_size"], Image.ANTIALIAS))
                self.images[file] = image
                image_list.append(file)
            except Exception:
              pass
          # Create an merged image of a file list if a file list exists
          if total_key not in self.images and len(image_list) > 1:
            img = merge_images(image_list)
            image = ImageTk.PhotoImage(img)
            self.images[total_key] = image



  # TODO: simplify/minimize this function:
  #       It should simply update the visual part of the gui according to the interaction happening with the gui 
  #       (for instance selecting an element or deleting a selected one) as well as update the clipboard display
  def update_clipboard(self):
    # Start by updating images that are being stored
    self.update_images()
    row, column = 0, 0

    # Clear the frame by destroying it and its children and create a new one
    # TODO: Fix index errors when deleting last element - Exception
    for child in self.frame.winfo_children():
      child.pack_forget()
    self.frame.destroy()
    self.frame = Frame(self.root)

    for idx, elements  in enumerate(self.clipboard._memory):
      # Extract text
      lable_text = ""
      use_image = False
      image = None
      images = [] # stores all paths of images that have to be stored
      for typ, data in elements:
        if typ == 13: # plain text
          lable_text = data
          break

        # TODO: This only works for a local machine. We will need to check if the image
        #       Can be found on this machine and if not REQUEST it from the server
        if typ == 15: # files
          use_image = True
          for file in data:
            lable_text += file
            # Handle multiple files when copying more than one image.
            # Create a list of all image
            if file in self.images:
              images.append(file)
            else: # If the file copied is not and image use a default placeholder for a file
              images.append("unknown_file_image")
   
      # Set bg color depending on if element is selected or not
      bg_color = "grey" if idx != self.clipboard._idx else "red"

      # Select an image if the current element is an image
      if use_image:
        # If only one image was found use that
        # If more images were found merge those into a single image
        image = self.images.get(images[0] if len(images) == 1 else lable_text, self.images["unknown_file_image"])

      # TODO: Fix lable size and text length is use_image is false.
      #       We want to create a compromise between readability and visually pleasing

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
  
  # Open a popup window for settings
  def open_settings(self):
    self.settings = Toplevel(self.root)
    self.settings.title("Settings")
    self.settings.geometry("{0}x{1}+{2}+{3}".format(
      int(self.window.width / 2), 
      int(self.window.height / 2), 
      self.window.x_offset * 2, 
      self.window.y_offset * 3)
    ) 

