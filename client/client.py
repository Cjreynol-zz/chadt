import logging as log

from chadt.chadt_exceptions import UsernameCurrentlyUnstableException, UsernameTooLongException
from chadt.connection import Connection
from chadt.connection_handler import ConnectionHandler
from chadt.constants import SERVER_NAME
from chadt.message import Message
from chadt.message_handler import MessageHandler
from chadt.message_type import MessageType
from chadt.system_message import SystemMessage


class Client(MessageHandler):
    """The controller of a user's chat connection.
    
    It makes its connection to the server on initialization, then waits 
    to be started up.

    """

    def __init__(self, server_host, server_port, system_message_queue):
        super().__init__(MessageType)

        self.username = ""
        self.username_stable = False  # indicates if username request is out

        self.message_out_queue = []
        self.connected_users = []
        self.system_message_queue = system_message_queue

        connection = Connection(server_port, server_host)
        self.server_connection = ConnectionHandler(self.username, connection, self.message_processing_queue, self.message_out_queue)

        log.info("Client created.")

    def start_client(self): 
        """Calls start on the various components that make up Client."""
        self.server_connection.start()
        super().start()
        log.info("Client started.")

    def stop_client(self):
        """Calls stop on the various components that make up Client."""
        self.server_connection.stop()
        super().stop()
        log.info("Client stopped.")

    def shutdown_client(self):
        """Calls shutdown on the various components that make up Client.
        Also creates a disconnect message for the server that is passed to
        the connection to the server.
        """
        disconnect_message = Message.construct_disconnect("", self.username, SERVER_NAME)
        self.server_connection.shutdown(disconnect_message)
        super().shutdown()
        log.info("Client shut down.")

    def send_username_request(self, username):
        """Verifies the username is a valid length, then calls for a request 
        message to be sent if so.
        """
        if self.is_username_valid_length(username):
            self.add_message_to_out_queue(username, SERVER_NAME, Message.construct_username_request)
            self.username_stable = False
        else:
            raise UsernameTooLongException()

    def add_message_to_out_queue(self, text, recipient, message_constructor = Message.construct_text):
        """Given text and recipient, constructs a message and adds it to the 
        queue for being sent.
        
        Accepts a message constructor so that other objects utilizing client 
        are insulated from needing to know about the Message class.
        """
        if self.username_stable:
            message = message_constructor(text, self.username, recipient)
            self.message_out_queue.append(message)
        else:
            raise UsernameCurrentlyUnstableException()

    def handle_text(self, message):
        """Constructs a system message from the chat text message."""
        system_message = SystemMessage.construct_text(message.get_display_string())
        self.system_message_queue.append(system_message)

    def handle_disconnect(self, message):
        """Constructs a system message from the disconnect message."""
        system_message = SystemMessage.construct_shutdown(message.get_display_string())
        self.system_message_queue.append(system_message)

    def handle_username_accepted(self, message):
        """Verifies the username is a valid length, and sets the proper 
        attributes.
        """
        username = message.text
        if self.is_username_valid_length(username):
            self.username = username
            self.server_connection.username = username
            self.username_stable = True
        else:
            raise UsernameTooLongException()

    def handle_username_rejected(self, message):
        """Constructs a system message from the username rejection message."""
        self.username_stable = True
        system_message = SystemMessage.construct_username_rejected(message.get_display_string())
        self.system_message_queue.append(system_message)

    def handle_temp_username_assigned(self, message):
        """Passes the message along to be treated as an accepted request."""
        self.handle_username_accepted(message)

    def handle_list_of_users(self, message):
        """Breaks the user string into a list, adds it to the list of other 
        users, and calls for a system message to be created.
        """
        list_of_users = message.text.split(',')
        self.connected_users  = self.connected_users + list_of_users
        self._send_system_message_user_update(message)

    def handle_user_connect(self, message):
        """Retrieves the new username from the message and calls for a 
        system message to be created.
        """
        username = message.text
        self.connected_users.append(username)
        self._send_system_message_user_update(message)

    def handle_user_name_change(self, message):
        """Retrieves the old and new usernames, updates the proper element in 
        the list of other users, and calls for a system message to be created.
        """
        old, new = message.text.split(',')

        # remove/replace new username in the same index, preserving order
        index = self.connected_users.index(old)
        self.connected_users.pop(index)
        self.connected_users.insert(index, new)

        self._send_system_message_user_update(message)

    def handle_user_disconnect(self, message):
        """Retrieves the disconnected username from the message and calls for 
        a system message to be created.
        """
        username = message.text
        self.connected_users.remove(username)
        self._send_system_message_user_update(message)

    def _send_system_message_user_update(self, message):
        """Constructs a system message from a user update messages."""
        system_message = SystemMessage.construct_user_list_update(message.get_display_string())
        self.system_message_queue.append(system_message)
