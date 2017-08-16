

class ZeroLengthMessageException(Exception):
    """
    Exception for when a socket receives a zero-length message when it 
    was expecting more.
    """
    
    def __init__(self, message):
        self.message = message
