from chadt.chadt_exceptions import UsernameCurrentlyUnstableException, UsernameTooLongException
from chadt.view_controller import ViewController

from client.client import Client
from client.client_chat_view import ClientChatView
from client.client_config_view import ClientConfigView


class ClientViewController(ViewController):
    
    def __init__(self):
        super().__init__()
        self.client = None

    def start_controller(self):
        self._setup_config_view()
        self.start()

    def quit(self):
        if self.client is not None:
            self.client.shutdown_client()
        super().quit()

    def handle_user_list_update(self, message):
        self.view.update_list_of_users(self.client.connected_users)
        self.view.display_new_text_message(message.text)

    def handle_username_rejected(self, message):
        self.view.warning_message("Username Rejected", "Username requested was rejected by the server.")

    def handle_shutdown(self, message):
        self.view.warning_message("Server Shutdown", "Server was shutdown, client shutting down now.")
        self.quit()

    def _setup_config_view(self):
        self.view = ClientConfigView()
        self.view.set_confirm_button_command(self._confirm_button)
        self.view.add_quit_function(self.quit)

    def _swap_to_chat_view(self):
        if self.view is not None:
            self.view.quit()
        self._setup_chat_view()

    def _setup_chat_view(self):
        self.view = ClientChatView()
        self.view.set_message_entry_button_commands(self._send_message_button)
        self.view.set_username_entry_button_commands(self._send_username_button)
        self.view.add_quit_function(self.quit)

    def _confirm_button(self, server_host_entry, server_port_entry):
        def f():
            server_port = server_port_entry.get()
            server_host = server_host_entry.get()
            if not self.is_valid_port_num(server_port):
                self.view.invalid_port_warning()
            else:
                self._swap_to_chat_view()
                self._create_client(server_host, int(server_port))
        return f

    def _create_client(self, server_host, server_port):
        self.client = Client(server_host, server_port, self.system_message_queue)
        self.client.start_client()

    def _send_message_button(self, message_entry):
        def f(event = None):
            recipient = self.view.get_users_box_selection()
            self.client.add_message_to_out_queue(message_entry.get(), recipient)
            self.view.clear_message_entry_box()
        return f

    def _send_username_button(self, username_entry):
        def f(event = None):
            try:
                requested_username = username_entry.get()
                self.client.send_username_request(requested_username)
                self.view.clear_username_entry_box()
            except UsernameCurrentlyUnstableException:
                self.view.warning_message("Username Unstable", "Username is currently being updated, please wait until it is set to try again.")
            except UsernameTooLongException:
                # should make a constants file for numbers like sender max length
                self.view.warning_message("Username Too Long", "Username requested is too long, please limit it to 16 chars")
                
        return f
