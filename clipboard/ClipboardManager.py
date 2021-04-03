## Data management
import win32clipboard
import ctypes
from ctypes import wintypes

## Utils
from functools import partial
import keyboard
import time
import pythoncom
import threading

## Local dependencies
try:
  import config as config
except:
  import clipboard.config as config
"""
#############################
######### History ###########
#############################
"""
class ClipboardMemory(object):
  def __init__(self):
    self._memory = []   # History of the clipboard
    self._idx    = -1   # Points towards the object that currently is in the clipboard
    self._req    = CBMRequest() # Technically doesn't belong in this class (Maybe change class name(?))
    
  def __contains__(self, item : any):
    return item in self._memory

  # Traverses backwards in the memory list. The index wraps around when surpassing the list on either side
  # This will also send a request to update the shared clipboard's index
  def backward(self): 
    self._idx = (self._idx - 1) % len(self._memory)
    self._req.update_index(self._idx)
    return self._memory[restore_idx]

  # Traverses forwards in the memory list. The index wraps around when surpassing the list on either side
  # This will also send a request to update the shared clipboard's index
  def forward(self):
    self._idx = (self._idx + 1) % len(self._memory)
    self.eq.update_index(self._idx)
    return self._memory[restore_idx]

  # Appends an element to the list and set the index towards the new element
  # This will also send a request to update the shared clipboard
  def add(self, data : set):
    self._memory.append(data)
    self._req.update_clipboard(data)
    self._idx = len(self._memory) - 1
    self._req.update_index(self._idx)

  # Delete the element at the index position
  # This will also send a request to update the shared clipboard
  def remove(self):
    if self._idx < 0 or not self._memory:
      return set()

    self._memory.pop(self._idx)
    self._req.delete_clipboard(self._idx)

    if self._idx >= len(self._memory):
      self._idx -= 1
      self._req.update_index(self._idx)

    if self._idx < 0 or not self._memory:
      return set()

    return self._memory[self._idx]

  # Delete the entire clipboard
  # This will also send a request to update the shared clipboard
  def clear(self):
    self._memory = []
    self._req.delete_clipboard()
    self._idx    = -1 
    self._req.update.index(self._idx)

  # Lists should be equal for every element but the newest one. Changes every element that differs to the new one
  # Does NOT send the updated clipboard version. This function exists to write an update from the server not to!
  def overwrite(self, memory : list, idx : int):
    self._memory = memory
    self._idx = idx


  

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
    win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, stg.data)
  except Exception:
    pass

# Returnes the data stored in the clipboard
def get_clipboard_data():
  # Open clipboard context and get first format_id
  win32clipboard.OpenClipboard()
  data = set()

  format_id = 0
  
  # Iterate over all format_ids and get the data for the valid ones
  while format_id := win32clipboard.EnumClipboardFormats(format_id):
    
    # Check if format id is allowed
    if format_id not in config.format_id_allow_set:
     continue
    
    # Get the current data for this format_id from the clipboard
    try:
      data.add((format_id, win32clipboard.GetClipboardData(format_id)))
    except Exception:
      print(format_id)

  win32clipboard.CloseClipboard()
  return data

# Stores any given and valid data in the clipboard
def update_clipboard_data(data):
  # Open clipboard context and clear it
  win32clipboard.OpenClipboard()
  win32clipboard.EmptyClipboard()

  for format_id, entry in data:
    try:
      if(format_id == 15):
        set_files_to_clipboard(entry)
      else:
        win32clipboard.SetClipboardData(format_id, entry)
    except Exception as e:
      print(e)
      print(format_id)

  win32clipboard.CloseClipboard()

"""
#############################
######### Keyboard ##########
#############################
"""
# Start function module this module
def start_clipboardManager():
  memory = ClipboardMemory()   
  
  check_for_updates = True
  def start_CBMRequest():
    req = CBMRequest()
    while check_for_updates:
      do_update, index = req.update_available()
      memory._idx = index
      if (do_update):
        memory.overwrite(req.get_clipboard(), index)
      time.sleep(1)
  request_thread = threading.Thread(target=start_CBMRequest)
  request_thread.start()

  def on_press_copy():
    time.sleep(0.3)
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

  def on_press_remove():
    update_clipboard_data(memory.remove())
    print("removed")

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
    ("ctrl+c",     on_press_copy),
    ("ctrl+alt+r", on_press_backward),
    ("ctrl+alt+f", on_press_forward),
    ("ctrl+alt+d", on_press_remove),
    ("ctrl+alt+c", on_press_clear),
    ("ctrl+alt+p", on_press_print)
  }

  # Create and add selector functions with addressing by number
  for id in range(10):
    hotkey_set.add(("ctrl+alt+{id}".format(id = id), partial(on_press_restore_id, id)))
  
  # Add hotkey listeners to the keyboard object
  for keys, func in hotkey_set:
    keyboard.add_hotkey(keys, func)

  # Wait until escape was pressed and end the programm
  keyboard.wait('esc')
  check_for_updates = False
  request_thread.join()




"""
#############################
######### Network ###########
#############################
"""

import requests
import pickle
class CBMRequest():

  def __init__(self):
    self.updateID = 0
    self.url = f"http://{config.ip}:{config.port}{{}}" 
    
  # Return the entire clipboard currently stored in the server
  def get_clipboard(self):
    res = requests.get(self.url.format("/clipboard"))
    clipboard = pickle.loads(res.content)
    res.close()
    return clipboard
    
  # Send a new value that will be added to the shared clipboard
  def update_clipboard(self, data : set):
    res = requests.post(self.url.format("/clipboard"), data=pickle.dumps(data))
    id = pickle.loads(res.content)
    self.updateID = id
    res.close()

  # Will clear either the entire clipboard if no index is specified or just remove a single element at a given index
  # If the index was invalid nothing will be removed and the updateID wont change.
  # If the index was valid the updateID is updated to the value returned from the server.
  def delete_clipboard(self, index : int=-1):
    query = ""
    if index >= 0:
      query = "?index={}".format(index)
    res = requests.delete(self.url.format("/clipboard") + query)
    id = pickle.loads(res.content)
    res.close()
    if (id >= 0):
      self.updateID = id
    
  # Update the current idnex of the shared clipboard. If the index was updated succesfully it is being returned. Else -1 is returned.
  def update_index(self, index : int):
    res = requests.post(self.url.format("/index"), data=pickle.dumps(index))
    index = pickle.loads(res.content)
    res.close()
    return index

  # Check if an update is available from the server. Return a tuple with the a bool and current index which can always change 
  # It will also update the current updateID of the client so this function only yields true for each ID once.
  def update_available(self):
    res = requests.get(self.url.format("/clipboard/available"))
    id, index = pickle.loads(res.content)
    update = self.updateID != id
    self.updateID = id
    res.close()
    return (update, index)

  def benchmark(self):
    times = []
    requests = 1000
    for i in range(requests):
      start = time.time()
      data = {(13, 'f"{base_url}/clipbasdasdoard"'), (1, b'f"{base_url}/casdasdlipboard"'), (7, b'f"{base_url}/cliasdasdpboard"')}
      self.update_clipboard(data)
      self.get_clipboard()
      times.append(time.time() - start)
      if (i % 100 == 0):
        self.delete_clipboard()
        print("{0} of requests finished".format(i))

    print("The average request took {0} seconds".format(sum(times) / len(times)))
    print("Longest request was the {0}-th request with {1} seconds.".format(times.index(max(times)), max(times)))
    print("Shortes request was the {0}-th request with {1} seconds.".format(times.index(min(times)), min(times)))
    print("Total duration for all {0} requests was {1} seconds".format(requests, sum(times)))




