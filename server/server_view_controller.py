from server.server import Server
from server.server_view import ServerView
from chadt.chadt_view_controller import ChadtViewController


class ServerViewController(ChadtViewController):

    def __init__(self):
        super().__init__(ServerView)
        self.server = None

    def confirm_button(self, entry_widget):
        def f():
            if not self.is_valid_port_num(entry_widget.get()):
                self.view.invalid_port_warning()
            else:
                self.create_server(int(entry_widget.get()))
                self.start_main_window()
        return f

    def create_server(self, port_num):
        self.server = Server(port_num)
        self.server.add_client_list_observer(self.client_list_update)
        self.server.add_message_in_queue_observer(self.display_new_text_message)
        self.server.start_server()

    def client_list_update(self):
        self.view.update_list_box(self.server.clients.keys())

    def quit(self):
        if self.server is not None:
            self.server.shutdown_server()
        self.view.quit()

    def display_new_text_message(self, message_queue):
        message = message_queue.pop(0)
        self.view.display_new_text_message(message.display_string())
