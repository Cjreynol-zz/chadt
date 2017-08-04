from server.server import Server
from server.server_view import ServerView


class ServerViewController:

    def __init__(self):
        self.server = None
        self.view = ServerView(self)
        self.view.start_mainloop()

    def confirm_button(self, entry_widget):
        def f():
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

