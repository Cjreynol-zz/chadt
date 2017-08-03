import logging as log
from server_view_controller import ServerViewController


def main():
    log.basicConfig(level=log.DEBUG)
    s = ServerViewController()

if __name__ == "__main__":
    main()
