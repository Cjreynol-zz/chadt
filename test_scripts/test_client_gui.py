import logging as log
from client.client_view_controller import ClientViewController


def main():
    log.basicConfig(level=log.DEBUG)
    c = ClientViewController()

if __name__ == "__main__":
    main()
