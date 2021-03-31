"""
Start: (Fixed Port)
Prüfe ob ein Server exestiert:
  Er exestiert: Mache nichts
  Er exestiert nicht: Werde der Server

Running:
Server im eigenen Netzwerk.
  Copy_Signal -> Sende CopiedClipboard an alle verknüpften Geräte.

End:
Server beendet sich:
  Es exestieren noch verknüpfte Geräte  -> Eins davon wird zum Server
  Es exestieren keine verknüpfte Geräte -> Beende den Server  

Properties:
  - TCP Server
  - Fixed Port
  - Implemented with sockets
"""
import socket
import select
import os
import time
from queue import Queue
import threading
from config import PORT, BUFFER_SIZE, CLIENT_ACCEPT_LEN

class Server(threading.Thread):
  # Create server that handels incoming connection and passes them to the slave manager
  def __init__(self):
    super().__init__()
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    self.connectTo = ('localhost', PORT)
    self.socket.bind(self.connectTo)
    self.slave_manager = SlaveManager()
    self.slave_manager.start()
  
  def run(self):
    self.socket.listen(CLIENT_ACCEPT_LEN)
    
    while True:
      try:
        clientsocket, address = self.socket.accept()
      except OSError:
        print("Closing server")
        break
      
      self.slave_manager.add_slave(clientsocket)
    
  def stop(self):
    self.slave_manager.shutdown()
    self.slave_manager.join()
    self.socket.close()

class SlaveManager(threading.Thread):
  # Create slave manager that handels all socket connections and incoming data
  def __init__(self):
    super().__init__()
    self.stop = False
    self.slaves = []
    
  def add_slave(self, slave):
    self.slaves.append(slave)

  def remove_slave(self, slave):
    print("Closing socket")
    slave.shutdown(socket.SHUT_RDWR)
    slave.close()
    self.slaves.remove(slave)

  def shutdown(self):
    self.stop = True
    time.sleep(1)
    for slave in self.slaves:
      slave.shutdown(socket.SHUT_RDWR)
      slave.close()
    

  def run(self):
    while not self.stop:
      updates = []
      try:
        ready_to_read, ready_to_write, in_error = [], [], []
        if self.slaves:
          ready_to_read, ready_to_write, in_error = select.select(self.slaves, self.slaves, [], 5)
        else:
          time.sleep(5)
      except select.error:
        print('connection error')

      for sock in ready_to_read:
        data = sock.recv(BUFFER_SIZE)
        # Check if connection is closed
        if not data:
          self.remove_slave(sock)
          ready_to_write.remove(sock)
          continue

        updates.append(data)
        # Give data to clipboard manager
        print('received:', data)

      for update in updates:
        for sock in ready_to_write:
          sock.send(update)

if __name__ == "__main__":
  server = Server()
  server.start()
  