import logging as log
import tkinter as tk

from server.server_view_controller import ServerViewController
from client.client_view_controller import ClientViewController


def main():
    root = tk.Tk()
    root.title("Chadt")

    server_button = tk.Button(root, text="Create Server", command=create_server)
    client_button = tk.Button(root, text="Create Client", command=create_client)

    server_button.grid(row=0, column=0)
    client_button.grid(row=0, column=1)

    tk.mainloop()

def create_server():
    s = ServerViewController()
    s.start_view()

def create_client():
    c = ClientViewController()
    c.start_view()

if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main()
