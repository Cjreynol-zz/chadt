import tkinter as tk


class ServerView:

    def __init__(self, controller):
        self.controller = controller
        self.root = self.initialize_window()
        self.add_port_selection_widgets()
        self.list_box = None

    def initialize_window(self):
        root = tk.Toplevel()
        root.title("Chadt Server")
        return root

    def add_port_selection_widgets(self):
        l = tk.Label(self.root, text="Choose Port:")
        e = tk.Entry(self.root)
        e.insert(0, "50000")
        b = tk.Button(self.root, text="Confirm", command=self.controller.confirm_button(e))

        l.grid(row=0, column=0)
        e.grid(row=0, column=1)
        b.grid(row=1, column=0)

    def clear_window(self):
        for widget in self.root.grid_slaves():
            widget.destroy()

    def add_control_widgets(self):
        l = tk.Label(self.root, text="Connected Clients:")

        self.list_box = tk.Listbox(self.root)
        sb = tk.Scrollbar(self.root, command=self.list_box.yview)

        l.pack()
        self.list_box.pack()
        sb.pack()

    def update_list_box(self, items):
        self.list_box.delete(0, tk.END)
        for item in items:
            self.list_box.insert(tk.END, item)
