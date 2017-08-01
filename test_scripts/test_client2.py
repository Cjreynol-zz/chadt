import logging as log
from client import Client

def main():
    log.basicConfig(level=log.DEBUG)
    c = Client("chad2", "localhost", 36003, 36004)
    c.start_client()

if __name__ == "__main__":
    main()
