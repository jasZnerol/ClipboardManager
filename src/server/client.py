import socket
from server.config import PORT

class Client(object):
  def __init__(self):
    self.socket = socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectTo = ('localhost', PORT)
    socket.connect(self.connectTo)

  def send(self, data):
    if isinstance(data, bytes):
      data = bytes(data)
    self.socket.sendall(data)

  def close(self):
    self.socket.close()
