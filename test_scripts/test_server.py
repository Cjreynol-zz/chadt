import logging as log
from server import Server

def main():
    log.basicConfig(level=log.DEBUG)
    s = Server()
    s.start_server()

if __name__ == "__main__":
    main()
