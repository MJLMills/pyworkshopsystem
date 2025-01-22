class Signal(object):

    def __init__(self):
        self.slots = []

    def connect(self, slot):
        if slot not in self.slots:
            self.slots.append(slot)

    def disconnect(self, slot):
        if slot in self.slots:
            self.slots.pop(self.slots.index(slot))

    def emit(self, **kwargs):
        for slot in self.slots:
            slot(**kwargs)

    def __str__(self):
        str_rep = self.__class__.__name__
        return str_rep