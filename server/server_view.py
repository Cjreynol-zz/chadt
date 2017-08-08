import tkinter as tk
from lib.chadt_view import ChadtView


class ServerView(ChadtView):

    def __init__(self, controller):
        super().__init__("Chadt Server", controller)
        self.list_box = None

    def add_config_widgets(self):
        l = tk.Label(self.root, text="Choose Port:")
        e = tk.Entry(self.root)
        e.insert(0, "50000")
        b = tk.Button(self.root, text="Confirm", command=self.controller.confirm_button(e))

        l.grid(row=0, column=0)
        e.grid(row=0, column=1)
        b.grid(row=1, column=0)

    def add_main_widgets(self):
        l = tk.Label(self.root, text="Connected Clients:")
        self.list_box = tk.Listbox(self.root)

        l.grid(row=0, column=0)
        self.list_box.grid(row=1, column=0)

    def update_list_box(self, items):
        self.list_box.delete(0, tk.END)
        for item in items:
            self.list_box.insert(tk.END, item)
