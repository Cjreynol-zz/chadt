import tkinter as tk


class ClientView:

    def __init__(self, controller):
        self.controller = controller
        self.root = self.initialize_window()
        self.add_config_widgets()
        self.text = None
        self.text_entry = None

    def start_mainloop(self):
        tk.mainloop()

    def initialize_window(self):
        root = tk.Tk()
        root.title("Chadt Client")
        return root

    def add_config_widgets(self):
        l1 = tk.Label(self.root, text="Choose Ports:")
        e1 = tk.Entry(self.root)
        e1.insert(0, "50001")
        e2 = tk.Entry(self.root)
        e2.insert(0, "50002")

        l2 = tk.Label(self.root, text="Choose Username:")
        e3 = tk.Entry(self.root)
        e3.insert(0, "Username")

        b = tk.Button(self.root, text="Confirm", command=self.controller.confirm_button(e3, e1, e2))
        
        l1.grid(row=0, column=0)
        e1.grid(row=0, column=1)
        e2.grid(row=0, column=2)
        
        l2.grid(row=1, column=0)
        e3.grid(row=1, column=1)

        b.grid(row=2, column=0)

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
