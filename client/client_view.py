import tkinter as tk
from chadt.chadt_view import ChadtView


class ClientView(ChadtView):

    def __init__(self, controller):
        super().__init__("Chadt Client", controller)
        self.text = None
        self.text_entry = None

    def add_config_widgets(self):
        l1 = tk.Label(self.root, text="Choose Username:")
        client_username_entry = tk.Entry(self.root)
        client_username_entry.insert(0, "Username")

        l2 = tk.Label(self.root, text="Choose Server host/port:")
        server_host_entry = tk.Entry(self.root)
        server_host_entry.insert(0, "localhost")
        server_port_entry = tk.Entry(self.root)
        server_port_entry.insert(0, "50000")

        b = tk.Button(self.root, text="Confirm", command=self.controller.confirm_button(client_username_entry, server_host_entry, server_port_entry))
        
        
        l1.grid(row=1, column=0)
        client_username_entry.grid(row=1, column=1)

        l2.grid(row=0, column=0)
        server_host_entry.grid(row=0, column=1)
        server_port_entry.grid(row=0, column=2)

        b.grid(row=3, column=0)

    def add_main_widgets(self):
        self.text = tk.Text(self.root, height=10, width=80)
        self.text.bind("<Key>", lambda x: "break") 
        # this^ bind effectively makes the text widget read-only
        scroll = tk.Scrollbar(self.root, command=self.text.yview)
        self.text["yscrollcommand"] = scroll.set

        self.text_entry = tk.Entry(self.root)
        self.text_entry.insert(0, "Enter messages here")
        self.root.bind("<Return>", self.controller.send_message_button(self.text_entry))
		
        b = tk.Button(self.root, text="Send Message", command=self.controller.send_message_button(self.text_entry))
        
        self.text.grid(row=0, column=0)
        scroll.grid(row=0, column=1)
        self.text_entry.grid(row=1, column=0)
        b.grid(row=1, column=1)

    def display_new_message(self, message):
        self.text.insert(tk.END, message+"\n")
        self.text.see(tk.END)   # "scrolls" to latest entry

    def clear_entry_box(self):
        self.text_entry.delete(0, tk.END)
