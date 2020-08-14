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
from server.config import PORT, MAX_DATA_LEN

class Server(object):

  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectTo = ('localhost', PORT)
    self.socket.bind(self.connectTo)
    self.socket.listen(5)
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
      while not self.stop:
        data = self.socket.recv(MAX_DATA_LEN)
        if data:
          print(data)
      self.socket.close()
                

if __name__ == "__main__":
  s = Server()
  s.start()