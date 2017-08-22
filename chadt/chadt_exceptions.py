
class ChadtBaseException(Exception):

    def __init__(self, message = ""):
        self.message = message


class ComponentShuttingDownException(ChadtBaseException):
    pass


class ComponentStoppingException(ChadtBaseException):
    pass


class UsernameCurrentlyUnstableException(ChadtBaseException):
    pass


class UsernameTooLongException(ChadtBaseException):
    pass


class ZeroLengthMessageException(ChadtBaseException):
    pass
