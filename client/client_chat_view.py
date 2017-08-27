from tkinter import Button, END, Entry, Label, Listbox, Scrollbar, Text

from chadt.view import View
from chadt.constants import ALL_NAME


class ClientChatView(View):
    
    WINDOW_TITLE = "Chadt Chat"
    CHAT_HEIGHT = 10
    CHAT_WIDTH = 80
    MESSAGE_DEFAULT = "Enter messages here"
    MESSAGE_BUTTON_LABEL = "Send message"
    USERNAME_DEFAULT = "Enter username here"
    USERNAME_BUTTON_LABEL = "Request username"
    MESSAGE_ALL_USER = "Send to all users"
    
    def __init__(self):
        super().__init__(self.WINDOW_TITLE)

        self.chat_window = None
        self.chat_scroll = None
        self.message_entry = None
        self.send_message_button = None
        self.username_entry = None
        self.send_username_button = None
        self.user_list = None

        self._initialize_widgets()
        self._place_widgets()

    def _initialize_widgets(self):
        self.chat_window = Text(self.root, height = self.CHAT_HEIGHT, width = self.CHAT_WIDTH)
        self.chat_window.bind("<Key>", lambda x: "break") 
        # this^ bind effectively makes the text widget read-only

        self.chat_scroll = Scrollbar(self.root, command = self.chat_window.yview)
        self.chat_window["yscrollcommand"] = self.chat_scroll.set

        self.message_entry = Entry(self.root)
        self.message_entry.insert(0, self.MESSAGE_DEFAULT)

        self.send_message_button = Button(self.root, text = self.MESSAGE_BUTTON_LABEL)

        self.username_entry = Entry(self.root)
        self.username_entry.insert(0, self.USERNAME_DEFAULT)

        self.send_username_button = Button(self.root, text = self.USERNAME_BUTTON_LABEL)
        
        self.user_list = Listbox(self.root)

    def _place_widgets(self):
        self.chat_window.grid(row = 0, column = 0)
        self.message_entry.grid(row = 2, column = 0)
        self.send_message_button.grid(row = 2, column = 1)
        self.username_entry.grid(row = 0, column = 1)
        self.send_username_button.grid(row = 1, column = 1)
        self.user_list.grid(row = 0, column = 2)

    def set_message_entry_button_commands(self, callback_generator):
        self.message_entry.bind("<Return>", callback_generator(self.message_entry))
        self.send_message_button["command"] = callback_generator(self.message_entry)

    def set_username_entry_button_commands(self, callback_generator):
        self.username_entry.bind("<Return>", callback_generator(self.username_entry))
        self.send_username_button["command"] = callback_generator(self.username_entry)

    def display_new_text_message(self, message):
        self.chat_window.insert(END, message+"\n")
        self.chat_window.see(END)

    def clear_message_entry_box(self):
        self.message_entry.delete(0, END)

    def clear_username_entry_box(self):
        self.username_entry.delete(0, END)

    def update_list_of_users(self, new_user_list):
        self.user_list.delete(0,  END)
        # all added for private messaging purposes
        self.user_list.insert(0, self.MESSAGE_ALL_USER)
        for user in new_user_list:
            self.user_list.insert(END, user)

    def get_users_box_selection(self):
        selected = self.user_list.curselection()
        index = 0
        if selected != ():
            index = selected

        recipient = self.user_list.get(index)
        if recipient == self.MESSAGE_ALL_USER:
            recipient = ALL_NAME
        return recipient
