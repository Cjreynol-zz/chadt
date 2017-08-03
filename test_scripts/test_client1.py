import logging as log
from client import Client

def main():
    log.basicConfig(level=log.DEBUG)
    c = Client("chad", "localhost", 50001, 50002)
    c.start_client()

if __name__ == "__main__":
    main()
