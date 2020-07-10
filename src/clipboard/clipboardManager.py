from pynput import keyboard
import clipboard


current = set() # Currently pressed key. Required for 
memory  = []    # Memory of the last stored clipboard

def on_press(key):

  rm_memory_modifier    = { keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('r') }
  clr_memory_modifier   = { keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('d') }
  print_memory_modifier = { keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('p') }
  
  # Quit program
  if key == keyboard.Key.esc:
    listener.stop()
    exit()

  # Check for copy combination
  if hasattr(key, 'char') and key.char == '\x03': # \x03 == CTRL + C
    data = clipboard.paste()
    if data not in memory:
      memory.append(data)

  # Check for remove key combination
  if key in rm_memory_modifier:
    current.add(key)
    if all(k in current for k in rm_memory_modifier):
      if memory != []:
        print("removed\t  \"" + str(memory.pop()) + "\"\tfrom clipboard")

  # Check for remove key combination
  if key in clr_memory_modifier:
    current.add(key)
    if all(k in current for k in clr_memory_modifier):
      memory.clear()
      print("memory cleared")

  # Check for print key combination
  if key in print_memory_modifier:
    current.add(key)
    if all(k in current for k in print_memory_modifier):
      print(memory)

def on_release(key):
  current.clear()

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
  listener.join()
