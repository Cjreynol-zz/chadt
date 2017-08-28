from chadt.view_controller import ViewController

from server.server import Server
from server.server_config_view import ServerConfigView
from server.server_running_view import ServerRunningView


class ServerViewController(ViewController):

    def __init__(self):
        super().__init__()
        self.server = None

    def start_controller(self):
        self._setup_config_view()
        self.start()

    def quit(self):
        if self.server is not None:
            self.server.shutdown_server()
        super().quit()

    def handle_user_list_update(self, message):
        self.view.update_list_box(self.server.clients.keys())
        self.view.display_new_text_message(message.text)

    def _setup_config_view(self):
        self.view = ServerConfigView()
        self.view.set_confirm_button_command(self._confirm_button)
        self.view.add_quit_function(self.quit)

    def _swap_to_running_view(self):
        if self.view is not None:
            self.view.quit()
        self._setup_running_view()

    def _setup_running_view(self):
        self.view = ServerRunningView()
        self.view.add_quit_function(self.quit)

    def _confirm_button(self, port_entry):
        def f():
            server_port = port_entry.get()
            if not self.is_valid_port_num(server_port):
                self.view.invalid_port_warning()
            else:
                self._create_server(int(server_port))
                self._swap_to_running_view()
        return f

    def _create_server(self, port_num):
        self.server = Server(port_num, self.message_processing_queue)
        self.server.start_server()
