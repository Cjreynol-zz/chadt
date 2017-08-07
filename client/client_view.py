import tkinter as tk
import tkinter.messagebox as tkmb


class ClientView:

    def __init__(self, controller):
        self.controller = controller
        self.root = self.initialize_window()
        self.add_config_widgets()
        self.text = None
        self.text_entry = None

    def initialize_window(self):
        root = tk.Toplevel()
        root.title("Chadt Client")
        return root

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

    def clear_window(self):
        for widget in self.root.grid_slaves():
            widget.destroy()

    def clear_entry_box(self):
        self.text_entry.delete(0, tk.END)
			
    def add_chat_widgets(self):
        self.text = tk.Text(self.root, height=10, width=80)
        e = tk.Entry(self.root)
        e.insert(0, "Enter messages here")
		
        self.text_entry = e

        b = tk.Button(self.root, text="Send Message", command=self.controller.send_message_button(e))
        
        self.root.bind("<Return>", self.controller.send_message_button(e))

        self.text.grid(row=0, column=0)
        e.grid(row=1, column=0)
        b.grid(row=1, column=1)

    def display_new_message(self, message):
        self.text.insert(tk.END, message+"\n")

    def not_an_int_warning(self):
        tkmb.showwarning("Invalid value", "Port selection entry is not an integer in port range(1024-65535).")
