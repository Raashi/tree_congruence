class CongruenceClass:
    class CongruenceClassIterator:
        def __init__(self, cls):
            self.cls = cls
            self.idx = -1

        def __next__(self):
            self.idx += 1
            if self.idx < len(self.cls):
                return self.cls[self.idx]
            raise StopIteration

    def __init__(self, nodes):
        self._nodes = sorted(nodes)
        self.string = '{' + ', '.join(self._nodes) + '}'
        self.hash = self.string.__hash__()

    def __str__(self):
        return self.string

    def __add__(self, other):
        if not isinstance(other, CongruenceClass):
            raise ValueError
        return CongruenceClass(self._nodes + other._nodes)

    def __iter__(self):
        return self.CongruenceClassIterator(self)

    def __getitem__(self, item):
        return self._nodes[item]

    def __eq__(self, other):
        return self.string == other.string

    def __len__(self):
        return len(self._nodes)

    def __lt__(self, other):
        return self.string < other.string

    def __hash__(self):
        return self.hash
