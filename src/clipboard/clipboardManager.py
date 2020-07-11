# Global dependencies
## Data management
import win32clipboard as clipboard
import ctypes
from ctypes import wintypes
## Utils
from functools import partial
import keyboard
import time
import pythoncom

# Local dependencies
import config



"""
#############################
######### History ###########
#############################
"""
class ClipboardMemory(object):
  def __init__(self):
    self._memory = []   # History of the clipboard
    self._idx    = -1   # Points towards the object that currently is in the clipboard
  
  def __contains__(self, item):
    return item in self._memory

  # Traverses backwards in the memory list
  def backward(self): 
    restore_idx = self._idx - 1
    if restore_idx < 0 or restore_idx >= len(self._memory):
      return set()
    
    self._idx -= 1
    return self._memory[restore_idx]

  # Traverses forwards in the memory list
  def forward(self):
    restore_idx = self._idx + 1
    if restore_idx < 0 or restore_idx >= len(self._memory):
      return set()
    self._idx += 1
    print(self._memory[restore_idx])
    return self._memory[restore_idx]

  # Appends an element after the current element in the clipboard. All other element after that one get deleted.
  def add(self, data):
    if len(self._memory) < 2:
      self._memory.append(data)
      self._idx += 1
      return

    while self._memory and self._idx < len(self._memory) - 1:
      self._memory.pop()
    self._idx = len(self._memory)
    self._memory.append(data)
    
  # Reset the memory and index to initialization state
  def clear(self):
    self._memory = []
    self._idx    = -1 


"""
#############################
######## Clipboard ##########
#############################
"""
# Implements the _DROPFILES struct from C++ in a python class.
class DROPFILES(ctypes.Structure):
  _fields_ = (('pFiles', wintypes.DWORD), # Offset of the file list
              ('pt',     wintypes.POINT), # Unused fields
              ('fNC',    wintypes.BOOL),  # as they are not required for out purposes
              ('fWide',  wintypes.BOOL))  # A value that indicates whether the file contains ANSI or Unicode characters. 
                                          # If the value is zero, the file contains ANSI characters. 
                                          # Otherwise, it contains Unicode characters.

# Sets a list of files to the clipboard.
def set_files_to_clipboard(file_list):
  offset = ctypes.sizeof(DROPFILES)
  length = sum(len(p) + 1 for p in file_list) + 1
  size   = offset + length * ctypes.sizeof(ctypes.c_wchar)
  
  # * Operator creates c_char array and () is the constructor function for c_char arrays
  buf    = (ctypes.c_char * size)() 
  
  # Create the dropfile object with the c_char array (buf) created above
  dropfile = DROPFILES.from_buffer(buf)

  # Initialize the fields defined in the Dropfile
  dropfile.pFiles, dropfile.fWide = offset, True

  for path in file_list:
    # Create c_wchar array class
    array_t         = ctypes.c_wchar * (len(path) + 1)
    # Create c_wchar array object from the class created above
    path_buf        = array_t.from_buffer(buf, offset)
    path_buf.value  = path
    offset         += ctypes.sizeof(path_buf)

  # Some python wrapper shit
  stg = pythoncom.STGMEDIUM()
  stg.set(pythoncom.TYMED_HGLOBAL, buf)
  try:
    clipboard.SetClipboardData(clipboard.CF_HDROP, stg.data)
  except:
    pass

# Returnes the data stored in the clipboard
def get_clipboard_data():
  # Open clipboard context and get first format_id
  clipboard.OpenClipboard()
  data = set()

  format_id = 0
  
  # Iterate over all format_ids and get the data for the valid ones
  while format_id := clipboard.EnumClipboardFormats(format_id):
    
    # Check if format id is allowed
    if format_id not in config.format_id_allow_set:
     continue
    
    # Get the current data for this format_id from the clipboard
    try:
      data.add((format_id, clipboard.GetClipboardData(format_id)))
    except:
      print(format_id)

  clipboard.CloseClipboard()
  return data

# Stores any given and valid data in the clipboard
def update_clipboard_data(data):
  # Open clipboard context and clear it
  clipboard.OpenClipboard()
  clipboard.EmptyClipboard()

  for format_id, entry in data:
    try:
      if(format_id == 15):
        set_files_to_clipboard(entry)
      else:
        clipboard.SetClipboardData(format_id, entry)
    except Exception as e:
      print(e)
      print(format_id)

  clipboard.CloseClipboard()



"""
#############################
######### Keyboard ##########
#############################
"""
# Start function for this module
def start_clipboardManager():
  memory = ClipboardMemory()   
  
  def on_press_copy():
    time.sleep(0.5)
    data = get_clipboard_data()
    if data not in memory:
      memory.add(data)
      print("copied")
    
  def on_press_backward():
    update_clipboard_data(memory.backward())
    print("backwards")

  def on_press_forward():
    update_clipboard_data(memory.forward())
    print("forward")

  def on_press_clear():
    memory.clear()
    print("memory cleared")

  def on_press_print():
    print(memory._memory)

  def on_press_restore_id(id):
    #print("Restoring id {id}".format(id = id))
    pass


  # Add hotkeys with corresponding function
  hotkey_set = {
    ('ctrl+c',     on_press_copy),
    ('ctrl+alt+r', on_press_backward),
    ('ctrl+alt+f', on_press_forward),
    ('ctrl+alt+c', on_press_clear),
    ('ctrl+alt+p', on_press_print)
  }

  # Create and add selector functions with addressing by number
  for id in range(10):
    hotkey_set.add(('ctrl+alt+{id}'.format(id = id), partial(on_press_restore_id, id)))
  
  # Add hotkey listeners to the keyboard object
  for keys, func in hotkey_set:
    keyboard.add_hotkey(keys, func)

  # Wait until escape was pressed and end the programm
  keyboard.wait('esc')

start_clipboardManager()
