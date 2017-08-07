from server.server import Server
from server.server_view import ServerView


class ServerViewController:

    def __init__(self):
        self.server = None
        self.view = None

    def start_view(self):
        self.view = ServerView(self)
        
    def confirm_button(self, entry_widget):
        def f():
            if not self.is_valid_port_num(entry_widget.get()):
                self.view.not_an_int_warning()
            else:
                self.create_server(int(entry_widget.get()))
                self.start_main_window()
        return f

    def create_server(self, port_num):
        self.server = Server(port_num)
        self.server.start_server()
        self.server.clients.observers.append(self.client_list_update)

    def start_main_window(self):
        self.view.clear_window()
        self.view.add_control_widgets()

    def client_list_update(self):
        self.view.update_list_box(self.server.clients.keys())

    def is_valid_port_num(self, num):
        return_value = True
        try:
            num = int(num)
            if num < 1024 or num > 65535:
                return_value = False
        except ValueError:
            return_value = False

        return return_value
