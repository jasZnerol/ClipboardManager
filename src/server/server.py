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
import threading
from config import PORT, MAX_DATA_LEN

class Server(object):

  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectTo = ('localhost', PORT)
    self.socket.bind(self.connectTo)
    self.socket.listen(MAX_ACCEPT_LEN)
    self.slaves = []
  
  def start(self):
    while True:
      # accept connections from outside
      clientsocket, address = self.socket.accept()
      # now do something with the clientsocket
      # in this case, we'll pretend this is a threaded server
      new_slave = Slave(clientsocket, address)
      new_slave.start()
      self.slaves.append(new_slave)

  def stop(self):
    for slave in self.slaves:
      slave.shutdown()

    for slave in self.slaves:
      slave.join()

class Slave(threading.Thread):
    def __init__(self, socket, address):
      super().__init__()
      self.socket = socket
      self.address = address

    def shutdown(self):
        self.socket.shutdown(socket.SHUT_RDWR)

    def run(self):
      while True:
        try:
          ready_to_read, ready_to_write, in_error = select.select([self.socket], [self.socket], [], 5)
        except select.error:
          self.socket.shutdown(socket.SHUT_RDWR)    # 0 = done receiving, 1 = done sending, 2 = both
          self.socket.close()
          # connection error event here, maybe reconnect
          print('connection error')
          break
        if len(ready_to_read) > 0:
          recv = self.socket.recv(2048)
          # do stuff with received data
          print('received:', recv)
        #if len(ready_to_write) > 0:
        #  # connection established, send some stuff
        #  conn.send('some stuff')


if __name__ == "__main__":
  server = Server()
  server.start()