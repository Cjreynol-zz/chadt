from client.client import Client
from client.client_view import ClientView
from lib.chadt_view_controller import ChadtViewController


class ClientViewController(ChadtViewController):
    
    def __init__(self):
        super().__init__(ClientView)
        self.client = None

    def confirm_button(self, username_entry, server_host_entry, server_port_entry):
        def f():
            if not self.is_valid_port_num(server_port_entry.get()):
                self.view.not_an_int_warning()
            else:
                self.create_client(username_entry.get(), server_host_entry.get(), int(server_port_entry.get()))
                self.start_main_window()
        return f

    def create_client(self, username, server_host, server_port):
        self.client = Client(username, server_host, server_port, False)
        self.client.start_client()
        self.client.message_output = self.display_new_message

    def display_new_message(self, message):
        self.view.display_new_message(message)

    def send_message_button(self, message_entry):
        def f(event = None):
	        self.client.message_queue.append(bytes(message_entry.get(), "utf-8"))
	        self.view.clear_entry_box()
        return f
