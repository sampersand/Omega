class omobj:
    def __init__(self, base, evalfunc = None):
        self.base = base
        self.evalfunc = evalfunc
    def __str__(self):
        return str(self.base)
    def __repr__(self):
        return repr(self.base)
    def __bool__(self):
        return bool(str(self))
    def eval(self, locls):
        print('attempting to eval',locls)
        return None
class oper(omobj):
    def __init__(self, base, priority, func):
        super().__init__(base)
        self.priority = priority
        self.func = func
    def __repr__(self):
        return 'oper({},{},{})'.format(self.base, self.priority, self.func)
    def __str__(self):
        return self.base
    def __lt__(self, other):
        return self.priority < other.priority
