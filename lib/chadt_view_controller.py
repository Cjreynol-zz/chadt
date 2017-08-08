
class ChadtViewController:
    
    def __init__(self, view):
        self.view = view(self)

    def start_view(self):
        self.view.start()

    def start_main_window(self):
        self.view.start_main_window()

    def is_valid_port_num(self, num):
        return_value = True
        try:
            num = int(num)
            if num < 0 or num > 65535:
                return_value = False
        except ValueError:
            return_value = False

        return return_value
