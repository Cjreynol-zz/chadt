from tkinter import Button, Entry, Label

from chadt.chadt_view import ChadtView


class ServerConfigView(ChadtView):

    WINDOW_TITLE = "Chadt Server Config"
    LABEL_TEXT = "Enter Port:"
    PORT_DEFAULT = "50000"
    CONFIRM_BUTTON_LABEL = "Confirm"

    def __init__(self):
        super().__init__(self.WINDOW_TITLE)

        self.label = None
        self.port_entry = None
        self.confirm_button = None
        
        self.initialize_widgets()
        self.place_widgets()

    def initialize_widgets(self):
        self.label = Label(self.root, text = self.LABEL_TEXT)

        self.port_entry = Entry(self.root)
        self.port_entry.insert(0, self.PORT_DEFAULT)

        self.confirm_button = Button(self.root, text = self.CONFIRM_BUTTON_LABEL)

    def place_widgets(self):
        self.label.grid(row=0, column=0)
        self.port_entry.grid(row=0, column=1)
        self.confirm_button.grid(row=1, column=0)

    def set_confirm_button_command(self, callback_generator):
        self.confirm_button["command"] = callback_generator(self.port_entry)
