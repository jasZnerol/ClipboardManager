from pynput import keyboard
import clipboard

memory  = []    # Memory of the last stored clipboards

def on_press(key):
  # Quit program
  if key == keyboard.Key.esc:
    listener.stop()
    exit()

  # Check for copy combination: CTRL + C
  if hasattr(key, 'char') and key.char == '\x03':  
    data = clipboard.paste()
    if data not in memory:
      memory.append(data)

  # Check for remove key combination: CTRL + ALT + R
  if hasattr(key, 'vk') and hasattr(key, 'char') and key.vk == 82 and key.char == None:
    if memory != []:
      print("removed\t  \"" + str(memory.pop()) + "\"\tfrom clipboard")

  # Check for clear key combination: CTRL + ALT + C
  if hasattr(key, 'vk') and hasattr(key, 'char') and key.vk == 67 and key.char == None:
    memory.clear()
    print("memory cleared")

  # Check for print key combination: CTRL + ALT + P
  if hasattr(key, 'vk') and hasattr(key, 'char') and key.vk == 80 and key.char == None:
    print(memory)


def on_release(key):
  pass

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
  listener.join()
