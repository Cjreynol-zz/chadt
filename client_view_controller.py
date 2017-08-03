from client import Client
from client_view import ClientView


class ClientViewController:
    
    def __init__(self):
        self.client = None
        self.view = ClientView(self)
        self.view.start_mainloop()

    def confirm_button(self, username_entry, port_entry1, port_entry2):
        def f():
            self.create_client(username_entry.get(), int(port_entry1.get()), int(port_entry2.get()))
            self.start_main_window()
        return f

    def create_client(self, username, receive_port, transmit_port):
        self.client = Client(username, receive_port, transmit_port, False)
        self.client.start_client()
        self.client.message_output = self.display_new_message

    def display_new_message(self, message):
        self.view.display_new_message(message)

    def start_main_window(self):
        self.view.clear_window()
        self.view.add_chat_widgets()

    def send_message_button(self, message_entry):
        return lambda: self.client.message_queue.append(bytes(message_entry.get(), "utf-8"))

