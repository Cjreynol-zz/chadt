from collections.abc import MutableMapping

class ObservedKeyListDict(MutableMapping):
    
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
        self.observers = []

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value
        self.notify_observers()

    def __delitem__(self, key):
        del self._dict[key]
        self.notify_observers()

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def notify_observers(self):
        for observer in self.observers:
            observer()

    def add_observer(self, observer):
        self.observers.append(observer)
