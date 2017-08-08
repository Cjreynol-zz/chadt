import logging as log
import tkinter as tk
from tkinter.messagebox import askokcancel

from server.server_view_controller import ServerViewController
from client.client_view_controller import ClientViewController


class LaunchWindow:

    def __init__(self):
        self.root = None

    def start_window(self):
        self.root = tk.Tk()
        self.root.title("Chadt")
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        server_button = tk.Button(self.root, text="Create Server", command=self.create_server)
        client_button = tk.Button(self.root, text="Create Client", command=self.create_client)

        server_button.grid(row=0, column=0)
        client_button.grid(row=0, column=1)

        self.root.mainloop()
        
    def quit(self):
        if askokcancel("Quit", "Do you want to quit Chadt?"):
            self.root.destroy()
    
    def create_server(self):
        s = ServerViewController()
        s.start_view()

    def create_client(self):
        c = ClientViewController()
        c.start_view()

def main():
    l = LaunchWindow()
    l.start_window()

if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main()
