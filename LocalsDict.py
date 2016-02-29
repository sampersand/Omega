from Group import group
class localsdict(dict):
    LAST_VAL = '$'
    RET_VAL = '$ret'
    BREAK_VAL = '$break'

    def __init__(self):
        super().__init__({})
        self.resetlast()
        self.resetret()

    def resetlast(self):
        import Group
        self[localsdict.LAST_VAL] = Group.group()

    def resetret(self):
        import Group
        self[localsdict.RET_VAL]  = Group.group()

    def __iter__(self):
        for i in super().__iter__():
            if not self[i].isnull():
                yield i

    def __str__(self):
        return '{' + ', '.join(repr(v) + ' : ' + str(self[v]) for v in self) + '}'

    def lastval():
        doc = "The last value that was evaluated"
        def fget(self):
            return self[localsdict.LAST_VAL]
        def fset(self, value):
            if __debug__:
                assert isinstance(value, group)
            self[localsdict.LAST_VAL] = value
        def fdel(self):
            self.resetlast()
        return locals()
    lastval = property(**lastval())

    def retval():
        doc = "The value to return"
        def fget(self):
            return self[localsdict.RET_VAL]
        def fset(self, value):
            if __debug__:
                assert isinstance(value, group)
            self[localsdict.RET_VAL] = value
        def fdel(self):
            self.resetret()
        return locals()
    retval = property(**retval())

    def hasret(self):
        return not self[localsdict.RET_VAL].base.isnull()

    def haslast(self):
        return not self[localsdict.LAST_VAL].base.isnull()

    def clear(self):
        ret = super().clear()
        self.gendefaults()
        return ret

    def onlyfuncs(self):
        ret = localsdict()
        from Objects import userfuncobj
        for e in self:
            if isinstance(self[e].base, userfuncobj):
                ret[e] = self[e]
        return ret

    def deepcopy(self):
        import copy
        return copy.deepcopy(self)