## Global dependencies
import threading
import time
from functools import partial
import keyboard

## Local dependencies
from clipboard.ClipboardManager import ClipboardMemory, CBMRequest # Classes
from clipboard.ClipboardManager import get_clipboard_data, update_clipboard_data # Functions
from clipboard.gui.Window import CBMWindow


# Start the application
def start():

  # Create memory and gui
  memory = ClipboardMemory()   
  gui = CBMWindow(memory)

  # Create client checking for serverside updates
  check_for_updates = True
  def start_update_checking():
    req = CBMRequest()
    while check_for_updates:
      do_update, index = req.update_available()
      memory._idx = index
      if (do_update):
        memory.overwrite(req.get_clipboard(), index)
      time.sleep(1)

  # Start threads
  request_thread = threading.Thread(target=start_update_checking)
  request_thread.start()

  # Create keybinds
  def on_press_copy():
    time.sleep(0.3)
    data = get_clipboard_data()
    if data not in memory:
      memory.add(data)
      gui.update_clipboard()
      print("copied")
    
  def on_press_backward():
    update_clipboard_data(memory.backward())
    gui.update_clipboard()
    print("backwards")

  def on_press_forward():
    update_clipboard_data(memory.forward())
    gui.update_clipboard()
    print("forward")

  def on_press_remove():
    update_clipboard_data(memory.remove())
    gui.update_clipboard()
    print("removed")

  def on_press_clear():
    memory.clear()
    gui.update_clipboard()
    print("memory cleared")

  def on_press_print():
    print(memory._memory)

  def on_press_toggle_gui():
    gui.toggle_visibility()
    print("toggle gui")

  def on_press_terminate():
    print("shutting down...")
    gui.shutdown()

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
    ("ctrl+alt+p", on_press_print),
    ("ctrl+alt+w", on_press_toggle_gui),
    ("esc", on_press_terminate)
  }

  # Create and add selector functions with addressing by number
  for id in range(10):
    hotkey_set.add(("ctrl+alt+{id}".format(id = id), partial(on_press_restore_id, id)))

  # Add hotkey listeners to the keyboard object
  for keys, func in hotkey_set:
    keyboard.add_hotkey(keys, func)

  # Wait until escape was pressed and end the programm. Escape will destroy the gui first.
  # then all threads are closed
  gui.run()
  check_for_updates = False
  request_thread.join()


if __name__ == "__main__":
  start()