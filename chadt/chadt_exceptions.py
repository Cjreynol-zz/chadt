
class ChadtBaseException(Exception):

    def __init__(self, message = ""):
        self.message = message


class ZeroLengthMessageException(ChadtBaseException):
    pass
    

class UsernameRejectedException(ChadtBaseException):
    pass


class UsernameTooLongException(ChadtBaseException):
    pass


class ComponentStoppingException(ChadtBaseException):
    pass


class ComponentShuttingDownException(ChadtBaseException):
    pass
