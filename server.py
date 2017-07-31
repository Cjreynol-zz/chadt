from threading import Thread
from socket import socket
import time



class Server(object):
  def __init__(self, port = 36000):
    self.port = port
    self.clients = dict()
    self.messages = []
    self.listening_socket = self.set_up_listening_socket(self.port)

    self.listen_thread = Thread(target = self.listen)
    self.relay_thread = Thread(target = self.relay_messages)

  def start_server(self):
      self.listen_thread.run()
      self.relay_thread.run()

  def relay_messages(self):
    while True:
        for address, client in self.clients.items():
            try:
                msg = client.sending_socket.recv(4096)
                self.relay_message(msg, address)
            except BlockingIOError:
                pass
        time.sleep(1)


  def relay_message(self, msg, sender):
    for address, client in self.clients.items():
      if sender != address:
        client.listening_socket.sendall(msg)

  def listen(self):
    while True:
      connection = self.listening_socket.accept()
      new_socket = connection[0]
      address = connection[1]
      if address in self.clients:
        new_socket.setblocking(False)
        self.clients[address].sending_socket = new_socket
      else:
        self.clients[address] = ClientConnection(address, new_socket)

  def set_up_listening_socket(self, port):
    s = socket()
    s.bind(("localhost", port))
    s.listen()
    return s
      


class ClientConnection(object):
  def __init__(self, address, listening_socket, sending_socket = None):
    self.address = address
    self.listening_socket = listening_socket
    self.sending_socket = sending_socket

