from pynput import keyboard
import clipboard
#import win32clipboard as clipboard

memory  = []    # Memory of the last stored clipboard

def on_press_STOP():
  listener.stop()
  exit()

def on_press_COPY():
  data = clipboard.paste()
  if data not in memory:
    memory.append(data)

def on_press_REMOVE():
  if memory != []:
      print("removed\t  \"" + str(memory.pop()) + "\"\tfrom clipboard")

def on_press_CLEAR():
  memory.clear()
  print("memory cleared")

def on_press_PRINT():
  print(memory)

# Add hotkeys with corresponding function
with keyboard.GlobalHotKeys({
  '<ctrl>+<alt>+s': on_press_STOP,
  '<ctrl>+c': on_press_COPY,
  '<ctrl>+<alt>+r': on_press_REMOVE,
  '<ctrl>+<alt>+c': on_press_CLEAR,
  '<ctrl>+<alt>+p': on_press_PRINT}) as listener: 
  listener.join()