from server.server import Server
from server.server_view import ServerView
from lib.chadt_view_controller import ChadtViewController


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
        self.server.start_server()
        self.server.clients.observers.append(self.client_list_update)

    def client_list_update(self):
        self.view.update_list_box(self.server.clients.keys())
