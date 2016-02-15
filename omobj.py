class omobj:
    def __init__(self, base, evalfunc = None):
        self.base = base
        self.evalfunc = evalfunc
    def __str__(self):
        return str(self.base)
    def __repr__(self):
        return 'omobj({},evalfunc={})'.format(repr(self.base), repr(self.evalfunc))
    def __bool__(self):
        return bool(str(self))
    def eval(self, grp, locls):
        print('attempting to eval grp \'{}\' with locls \'{}\''.format(grp, locls))
        if self.evalfunc == None:
            print('evalfunc is none, returning self.base ({})'.format(self.base))
            return self.base
        return None
class oper(omobj):
    def __init__(self, base, priority, evalfunc):
        super().__init__(base, evalfunc)
        self.priority = priority
    def __repr__(self):
        return 'oper({},{},{})'.format(self.base, self.priority, self.func)
    def __str__(self):
        return self.base
    def __lt__(self, other):
        return self.priority < other.priority
