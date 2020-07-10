from pynput import keyboard
import clipboard
import win32clipboard as clipboard
clipboard.OpenClipboard()
def getClipboardData():
  data = None
  types = [
    'CF_TEXT', 'CF_BITMAP', 
    'CF_METAFILEPICT',  'CF_SYLK',
    'CF_DIF', 'CF_TIFF', 'CF_OEMTEXT',
    'CF_DIB', 'CF_PALETTE',  'CF_PENDATA',
    'CF_RIFF',  'CF_WAVE',  'CF_UNICODETEXT', 
    'CF_ENHMETAFILE',  'CF_HDROP',  'CF_LOCALE',  
    'CF_DIBV5',  'CF_MAX', 'CF_OWNERDISPLAY',  
    'CF_DSPTEXT',  'CF_DSPBITMAP', 'CF_DSPMETAFILEPICT', 
    'CF_DSPENHMETAFILE'
  ]
  
  the_type = None
  for _type in types:
    try:
      data = clipboard.GetClipboardData(_type)
      the_type = _type
      print("reached")
      break
    except:
      pass
  return (data, the_type)
print(getClipboardData())

memory  = []    # Memory of the last stored clipboards



exit()
def on_press_ESC():
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
  '<esc>': on_press_ESC,
  '<ctrl>+c': on_press_COPY,
  '<ctrl>+<alt>+r': on_press_REMOVE,
  '<ctrl>+<alt>+c': on_press_CLEAR,
  '<ctrl>+<alt>+p': on_press_PRINT}) as listener: 
  listener.join()