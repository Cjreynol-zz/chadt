

class ObservedList:
    
    def __init__(self, *args, **kwargs):
        self._list = list(*args, **kwargs)
        self.observers = []

    def append(self, value):
        self._list.append(value)
        self.notify_observers()

    def __len__(self):
        return len(self._list)

    def notify_observers(self):
        for observer in self.observers:
            observer(self._list)

    def add_observer(self, observer):
        self.observers.append(observer)
