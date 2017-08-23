from tkinter import Toplevel
from tkinter.messagebox import showwarning

class ChadtView:

    def __init__(self, window_title):
        self.root = self.initialize_root(window_title)

    def initialize_root(self, window_title):
        root = Toplevel()
        root.title(window_title)
        return root

    def add_quit_function(self, function):
        self.root.protocol("WM_DELETE_WINDOW", function)

    def warning_message(self, title, warning_message):
        showwarning(title, warning_message)

    def invalid_port_warning(self):
        self.warning_message("Invalid value", "Port selection entry is not an integer in port range(0-65535).")

    def quit(self):
        self.root.destroy()
