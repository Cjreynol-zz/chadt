

class ObservedList:
    
    def __init__(self, *args, **kwargs):
        self._list = list(*args, **kwargs)
        self.observers = []

    def insert(self, index, value):
        self._list.insert(index, value)

    def remove(self, value):
        self._list.remove(value)
        self.notify_observers()

    def append(self, value):
        self._list.append(value)
        self.notify_observers()

    def clear(self):
        self._list.clear()

    def replace(self, old_value, new_value):
        index = self._list.index(old_value)
        self._list.pop(index)
        self._list.insert(index, new_value)
        self.notify_observers()

    def merge(self, other_list):
        self._list = self._list + other_list
        self.notify_observers()

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def notify_observers(self):
        for observer in self.observers:
            observer(self._list)

    def add_observer(self, observer):
        self.observers.append(observer)
