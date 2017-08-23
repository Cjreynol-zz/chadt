from tkinter import Button, END, Label, Listbox, Scrollbar, Text

from chadt.chadt_view import ChadtView


class ServerRunningView(ChadtView):
    
    WINDOW_TITLE = "Chadt Server"
    LABEL_TEXT = "Connected Clients:"
    CHAT_HEIGHT = 10
    CHAT_WIDTH = 80

    def __init__(self):
        super().__init__(self.WINDOW_TITLE)

        self.label = None
        self.user_list = None
        self.chat_log = None
        self.chat_scroll = None

        self.initialize_widgets()
        self.place_widgets()

    def initialize_widgets(self):
        self.label = Label(self.root, text = self.LABEL_TEXT)

        self.user_list = Listbox(self.root)

        self.chat_log = Text(self.root, height = self.CHAT_HEIGHT, width = self.CHAT_WIDTH)
        self.chat_log.bind("<Key>", lambda x: "break")
        # this^ bind effectively makes the text widget read-only

        self.chat_scroll = Scrollbar(self.root, command=self.chat_log.yview)
        self.chat_log["yscrollcommand"] = self.chat_scroll.set

    def place_widgets(self):
        self.label.grid(row = 0, column = 0)
        self.user_list.grid(row = 1, column = 0)
        self.chat_log.grid(row = 1, column = 1)

    def update_list_box(self, items):
        self.user_list.delete(0, END)
        for item in items:
            self.user_list.insert(END, item)

    def display_new_text_message(self, message):
        self.chat_log.insert(END, message+"\n")
        self.chat_log.see(END)
