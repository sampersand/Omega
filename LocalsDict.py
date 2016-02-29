from Group import group
class localsdict(dict):
    IVALS = '$ivals'
    LAST_VAL = '$'
    RET_VAL = '$ret'
    BREAK_VAL = '$break'

    def __new__(self, useIvals = True):
        return super().__new__(self)

    def __init__(self, useIvals = True):
        super().__init__(dict())
        if useIvals:
            self.resetivals()

    def resetivals(self):
        import Group
        self.ivals = localsdict(False)
        self.ivals[localsdict.LAST_VAL] = Group.group()
        self.ivals[localsdict.RET_VAL] = Group.group()

    def __iter__(self):
        for i in super().__iter__():
            if isinstance(self[i], dict) or not self[i].isnull():
                yield i

    def __str__(self):
        return '{' + ', '.join(repr(v) + ' : ' + str(self[v]) for v in self) + '}'

    def ivals():
        doc = "The values used by the program to track stuff"
        def fget(self):
            return self[localsdict.IVALS]
        def fset(self, value):
            self[localsdict.IVALS] = value
        def fdel(self):
            self[localsdict.IVALS].clear()
        return locals()
    ivals = property(**ivals())

    def clear(self):
        ret = super().clear()
        ret.resetivals()
        return ret

    def onlyfuncs(self):
        ret = localsdict()
        from Objects import userfuncobj
        for e in self:
            if not isinstance(self[e], dict) and isinstance(self[e].base, userfuncobj):
                ret[e] = self[e]
        return ret

    def deepcopy(self):
        import copy
        return copy.deepcopy(self)

    def last():
        doc = "The last value evaluated"
        def fget(self): return self.ivals[localsdict.LAST_VAL]
        def fset(self, value): self.ivals[localsdict.LAST_VAL] = value
        def fdel(self): self.ivals[localsdict.LAST_VAL] = group()
        return locals()
    last = property(**last())
    def ret():
        doc = "The value to return"
        def fget(self): return self.ivals[localsdict.RET_VAL]
        def fset(self, value): self.ivals[localsdict.RET_VAL] = value
        def fdel(self): self.ivals[localsdict.RET_VAL] = group()
        return locals()
    ret = property(**ret())






















