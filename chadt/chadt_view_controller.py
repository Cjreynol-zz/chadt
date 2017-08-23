

class ChadtViewController:
    
    def __init__(self):
        self.view = None

    def assign_view(self, view):
        self.view = view

    def is_valid_port_num(self, num):
        return_value = True
        try:
            num = int(num)
            if num <= 0 or num > 65535:
                return_value = False
        except ValueError:
            return_value = False

        return return_value

    def quit(self):
        raise NotImplementedError("Needs to be implemented.")
