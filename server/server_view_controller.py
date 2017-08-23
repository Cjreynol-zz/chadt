from chadt.chadt_view_controller import ChadtViewController

from server.server import Server
from server.server_config_view import ServerConfigView
from server.server_running_view import ServerRunningView


class ServerViewController(ChadtViewController):

    def __init__(self):
        super().__init__()
        self.server = None

    def start_controller(self):
        self.setup_config_view()

    def setup_config_view(self):
        self.view = ServerConfigView()
        self.view.set_confirm_button_command(self.confirm_button)
        self.view.add_quit_function(self.quit)

    def swap_to_running_view(self):
        self.view.quit()
        self.setup_running_view()

    def setup_running_view(self):
        self.view = ServerRunningView()
        self.view.add_quit_function(self.quit)

    def confirm_button(self, port_entry):
        def f():
            server_port = port_entry.get()
            if not self.is_valid_port_num(server_port):
                self.view.invalid_port_warning()
            else:
                self.create_server(int(server_port))
                self.swap_to_running_view()
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
