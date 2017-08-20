from tkinter import Toplevel
from tkinter.messagebox import showwarning

class ChadtView:

    def __init__(self, window_title, controller):
        self.controller = controller
        self.root = self.initialize_root(window_title)

    def initialize_root(self, window_title):
        root = Toplevel()
        root.title(window_title)
        root.protocol("WM_DELETE_WINDOW", self.controller.quit)
        return root

    def clear_widgets(self):
        for widget in self.root.grid_slaves():
            widget.destroy()

    def warning_message(self, title, warning_message):
        showwarning(title, warning_message)

    def invalid_port_warning(self):
        self.warning_message("Invalid value", "Port selection entry is not an integer in port range(0-65535).")

    def start(self):
        self.add_config_widgets()

    def add_config_widgets(self):
        raise NotImplementedError("Needs to be implemented.")

    def start_main_window(self):
        self.clear_widgets()
        self.add_main_widgets()

    def add_main_widgets(self):
        raise NotImplementedError("Needs to be implemented.")

    def quit(self):
        self.root.destroy()
