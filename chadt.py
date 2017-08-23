import logging as log
import tkinter as tk
from tkinter.messagebox import askokcancel

from client.client_view_controller import ClientViewController

from server.server_view_controller import ServerViewController


class LaunchWindow:

    def __init__(self):
        self.root = None
        self.main_window = None
        self.child_controllers = []

    def start_tkinter(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def start_window(self):
        self.main_window = tk.Tk()
        self.main_window.title("Chadt")
        
        self.main_window.protocol("WM_DELETE_WINDOW", self.quit)

        server_button = tk.Button(self.main_window, text="Create Server", command=self.create_server)
        client_button = tk.Button(self.main_window, text="Create Client", command=self.create_client)

        server_button.grid(row=0, column=0)
        client_button.grid(row=0, column=1)

        self.root.mainloop()
        
    def quit(self):
        self.main_window.destroy()
    
    def create_server(self):
        s = ServerViewController()
        s.start_controller()

    def create_client(self):
        c = ClientViewController()
        c.start_controller()

def main():
    l = LaunchWindow()
    l.start_tkinter()
    l.start_window()

if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main()
