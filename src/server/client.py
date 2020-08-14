import socket
from config import PORT

class Client(object):
  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectTo = ('localhost', PORT)
    self.socket.connect(self.connectTo)

  def send(self, data):
    if not isinstance(data, bytes):
      data = bytes(data, "utf-8")
    self.socket.sendall(data)

  def close(self):
    self.socket.close()
