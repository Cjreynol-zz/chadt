from client.client import Client
from client.client_view import ClientView


class ClientViewController:
    
    def __init__(self):
        self.client = None

    def start_view(self):
        self.view = ClientView(self)

    def confirm_button(self, username_entry, port_entry1, port_entry2, server_host_entry, server_port_entry):
        def f():
            self.create_client(username_entry.get(), int(port_entry1.get()), int(port_entry2.get()), server_host_entry.get(), int(server_port_entry.get()))
            self.start_main_window()
        return f

    def create_client(self, username, receive_port, transmit_port, server_host, server_port):
        self.client = Client(username, receive_port, transmit_port, server_host, server_port, False)
        self.client.start_client()
        self.client.message_output = self.display_new_message

    def display_new_message(self, message):
        self.view.display_new_message(message)

    def start_main_window(self):
        self.view.clear_window()
        self.view.add_chat_widgets()

    def send_message_button(self, message_entry):
        def f(event = None):
	        self.client.message_queue.append(bytes(message_entry.get(), "utf-8"))
	        self.view.clear_entry_box()
        return f

