from pynput import keyboard 
import win32clipboard


memory = []
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardText('testing 123')
print(str(win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)))
exit()
def on_press(key):  
  if hasattr(key, 'char') and key.char == 'q':
      exit()
  
  # Check for copy combination
  if hasattr(key, 'char') and key.char == '\x03': # \x03 == CTRL + C
    try:
      print(win32clipboard.GetClipboardData(win32clipboard.CF_TEXT))
      memory.append(win32clipboard.GetClipboardData(win32clipboard.CF_TEXT))
    except:
      pass
    print("COPY")

  # Check for paste combination
  if hasattr(key, 'char') and key.char == 'V': # == SHIFT + V
    if memory != []:
      print("removed", memory.pop(), "from clipboard")
    print("Paste")

def on_release(key):
  pass
# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
  listener.join()
