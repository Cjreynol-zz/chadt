from chadt.chadt_view_controller import ChadtViewController

from client.client import Client
from client.client_view import ClientView


class ClientViewController(ChadtViewController):
    
    def __init__(self):
        super().__init__(ClientView)
        self.client = None

    def confirm_button(self, server_host_entry, server_port_entry):
        def f():
            server_port = server_port_entry.get()
            if not self.is_valid_port_num(server_port):
                self.view.not_an_int_warning()
            else:
                self.create_client(server_host_entry.get(), int(server_port))
                self.start_main_window()
        return f

    def create_client(self, server_host, server_port):
        self.client = Client(server_host, server_port)
        self.client.add_message_in_queue_observer(self.display_new_text_message)
        self.client.start_client()

    def display_new_text_message(self, message_queue):
        message = message_queue.pop(0)
        self.view.display_new_text_message(message.display_string())

    def send_message_button(self, message_entry):
        def f(event = None):
            self.client.add_message_to_out_queue(message_entry.get())
            self.view.clear_entry_box()
        return f

    def quit(self):
        if self.client is not None:
            self.client.shutdown_client()
        self.view.quit()

    def update_username_button(self, username_entry):
        def f():
            requested_username = username_entry.get()
            self.client.send_username_request(requested_username)
        return f
