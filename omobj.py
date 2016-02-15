class oper:
    def __init__(self, value, priority, func):
        self.value = value
        self.priority = priority
        self.func = func
    def __repr__(self):
        return 'oper({},{},{})'.format(self.value, self.priority, self.func)
    def __str__(self):
        return self.value
    def __lt__(self, other):
        return self.priority < other.priority
