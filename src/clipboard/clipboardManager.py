from functools import partial
import win32clipboard as clipboard

import time



def get_clipboard_data():
  clipboard.OpenClipboard()
  data = set()

  format_id = clipboard.EnumClipboardFormats(0)
  while format_id:
    try:
      data.add((format_id, clipboard.GetClipboardData(format_id)))
    except:
      print(format_id)
    format_id = clipboard.EnumClipboardFormats(format_id)
  
  clipboard.CloseClipboard()
  return data

def update_clipboard_data(data):
  clipboard.OpenClipboard()
  for format_id, entry in data:
    try:
      clipboard.SetClipboardData(format_id, entry)
    except:
      print(format_id, entry)

  clipboard.CloseClipboard()

memory  = []    # Memory of the last stored clipboards

def on_press_esc():
  listener.stop()
  exit()

def on_press_copy():
  time.sleep(0.5)
  data = get_clipboard_data()
  if data not in memory:
    memory.append(data)

def on_press_restore():
  print("rea")
  if not memory:
    return
  data = memory.pop()
  update_clipboard_data(data)

def on_press_clear():
  memory.clear()
  print("memory cleared")

def on_press_print():
  print(memory)

def on_press_restore_id(id):
  print("Restoring id {id}".format(id = id))

# Add hotkeys with corresponding function
hotkey_map = {
  '<esc>': on_press_esc,
  '<ctrl>+c': on_press_copy,
  '<ctrl>+<alt>+r': on_press_restore,
  '<ctrl>+<alt>+c': on_press_clear,
  '<ctrl>+<alt>+p': on_press_print
}

for id in range(10):
  hotkey_map['<ctrl>+<alt>+{id}'.format(id = id)] = partial(on_press_restore_id, id)

with keyboard.GlobalHotKeys(hotkey_map) as listener: 
  listener.join()

