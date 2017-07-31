from threading import Thread
from socket import socket
import time


class Client(object):

  SERVER_ADDRESS = ("localhost", 36000)

  def __init__(self, host, listenport, sendport):
    self.listen_socket = self.setup_socket((host, listenport))
    self.send_socket = self.setup_socket((host, sendport))
    self.listen_thread = Thread(target = self.listen)
    self.send_thread = Thread(target = self.send)
    self.message_queue = []

  def listen(self):
    while True:
      message_from_server = self.listen_socket.recv(4096)
      print("\n" + message_from_server.decode().strip() + "\n>>>")

  def send(self):
    while True:
      if len(self.message_queue) > 0:
        self.send_socket.sendall(self.message_queue.pop(0))
      else:
        time.sleep(1)

  def running(self):
    self.listen_thread.start()
    self.send_thread.start()

    while True:
      message = input(">>>")
      self.message_queue.append(bytes(message, "utf-8"))

  def setup_socket(self, address):
    s = socket()
    s.bind(address)
    s.connect(self.SERVER_ADDRESS)
    return s

