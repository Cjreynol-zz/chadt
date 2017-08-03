import logging as log
from client import Client

def main():
    log.basicConfig(level=log.DEBUG)
    c = Client("chad2", "localhost", 50003, 50004)
    c.start_client()

if __name__ == "__main__":
    main()
