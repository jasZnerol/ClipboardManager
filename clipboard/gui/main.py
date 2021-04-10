import eel
eel.init('html')  # Give folder containing web files
import threading

## NOTE:
# The principle is that we create function which return value is then handled by a javascript function
# Therefore if we want to update the clipboard all we have to do is to return the clipboard and then let javascript
# handle the given data. This goes both ways. We can @eel.expose() a funciton in python and eel.expose(a function) in js



def update_clipboard(clipboard):
  eel.update_clipboard(clipboard)




def start_gui():
  eel.start('index.html', size=(800, 600))    # Start


if __name__ == '__main__':
  gui_thread = threading.Thread(target=start_gui)
  gui_thread.start()
  import time
  time.sleep(2)
  print("updating...")
  update_clipboard([1,2,3,4,5])
  gui_thread.join()


