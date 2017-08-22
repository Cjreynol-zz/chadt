import tkinter as tk

from chadt.chadt_view import ChadtView
from chadt.message import Message


class ClientView(ChadtView):
    
    WINDOW_TITLE = "Chadt Client"
    MESSAGE_ALL_USER = "Send to all users"

    def __init__(self, controller):
        super().__init__(ClientView.WINDOW_TITLE, controller)
        self.text = None
        self.message_entry = None
        self.username_entry = None
        self.users_box = None

    def add_config_widgets(self):

        l2 = tk.Label(self.root, text="Choose Server host/port:")
        server_host_entry = tk.Entry(self.root)
        server_host_entry.insert(0, "localhost")
        server_port_entry = tk.Entry(self.root)
        server_port_entry.insert(0, "50000")

        b = tk.Button(self.root, text="Confirm", command=self.controller.confirm_button(server_host_entry, server_port_entry))
        
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

        self.message_entry = tk.Entry(self.root)
        self.message_entry.insert(0, "Enter messages here")
        self.message_entry.bind("<Return>", self.controller.send_message_button(self.message_entry))
        send_message_button = tk.Button(self.root, text="Send Message", command=self.controller.send_message_button(self.message_entry))

        self.username_entry = tk.Entry(self.root)
        self.username_entry.insert(0, "Enter username here")
        self.username_entry.bind("<Return>", self.controller.update_username_button(self.username_entry))
        update_username_button = tk.Button(self.root, text="Update Username", command=self.controller.update_username_button(self.username_entry))
        
        self.users_box = tk.Listbox(self.root)

        self.text.grid(row=0, column=0)
        scroll.grid(row=0, column=1)

        self.users_box.grid(row=0, column=2)
        self.username_entry.grid(row=0, column=1)
        update_username_button.grid(row=1, column=1)

        self.message_entry.grid(row=2, column=0)
        send_message_button.grid(row=2, column=1)

    def display_new_text_message(self, message):
        self.text.insert(tk.END, message+"\n")
        self.text.see(tk.END)

    def clear_message_entry_box(self):
        self.message_entry.delete(0, tk.END)

    def clear_username_entry_box(self):
        self.username_entry.delete(0, tk.END)

    def update_list_of_users(self, user_list):
        self.users_box.delete(0,  tk.END)
        # all added for private messages purposes
        self.users_box.insert(0, ClientView.MESSAGE_ALL_USER)
        for user in user_list:
            self.users_box.insert(tk.END, user)

    def get_users_box_selection(self):
        selected = self.users_box.curselection()
        index = 0
        if selected != ():
            index = selected
        recipient = self.users_box.get(index)
        if recipient == ClientView.MESSAGE_ALL_USER:
            recipient = Message.ALL_NAME
        return recipient
