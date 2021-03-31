import socket
import select
import threading
import time
from queue import Queue
from config import PORT, BUFFER_SIZE

class Client(threading.Thread):
  def __init__(self):
    super().__init__()
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectTo = ('localhost', PORT)
    self.socket.connect(self.connectTo)
    self.stop = False
    self.server_updates = Queue()
    self.clipboard_updates = Queue()
    
  def shutdown(self):
    self.stop = True
    time.sleep(1) # wait for select in while-loop in run to finish
    self.socket.shutdown(socket.SHUT_RDWR)
    self.socket.close()
    

  # The server has noticed an update. Add the data from the server to the local clipboard manager.
  def get_server_update(self):
    return self.server_updates.get()
  
  # The local clipboard manager has noticed an update. Add the data from the local clipboard to the server thus to the other local clipboard managers.
  def add_clipboard_update(self, data):
    self.clipboard_updates.put(data)  

  def run(self):
    while not self.stop:
      try:
        ready_to_read, ready_to_write, in_error = select.select([self.socket], [self.socket], [], 5)
      except select.error:
        print('connection error')

      if ready_to_read:
        data = self.socket.recv(BUFFER_SIZE)
        # Check if connection is closed
        if not data:
          self.shutdown()

        self.server_updates.put(data)
        print('received:', data)
      
      if ready_to_write:
        while not self.clipboard_updates.empty():
          self.socket.send(self.clipboard_updates.get())

  
    

