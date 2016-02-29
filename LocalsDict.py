from Group import group
from Objects import userfuncobj
import copy
class localsdict(dict):
    IVALS = '$ivals'
    LAST_VAL = '$'
    RET_VAL = '$ret'
    ESCAPE_VAL = '$esc'

    def __new__(self, control, useIvals = True):
        return super().__new__(self)

    def __init__(self, control, useIvals = True):
        super().__init__(dict())
        self.control = control
        if useIvals:
            self.resetivals()

    def resetivals(self):
        self[localsdict.IVALS] = localsdict(self.control, False)
        for val in (localsdict.LAST_VAL, localsdict.RET_VAL, localsdict.ESCAPE_VAL):
            self[localsdict.IVALS][val] = group(control = self.control)

    def __iter__(self):
        for i in super().__iter__():
            if isinstance(self[i], dict) or not self[i].isnull():
                yield i

    def __str__(self):
        return '{' + ', '.join(repr(v) + ' : ' + str(self[v]) for v in self) + '}'

    def clear(self):
        ret = super().clear()
        ret.resetivals()
        return ret

    def onlyfuncs(self):
        ret = localsdict(self.control)
        for e in self:
            if not isinstance(self[e], dict) and isinstance(self[e].base, userfuncobj):
                ret[e] = self[e]
        return ret

    def deepcopy(self):
        return copy.deepcopy(self)

    def last():
        doc = "The last value evaluated"
        def fget(self): return self[localsdict.IVALS][localsdict.LAST_VAL]
        def fset(self, value): self[localsdict.IVALS][localsdict.LAST_VAL] = value
        def fdel(self): self[localsdict.IVALS][localsdict.LAST_VAL] = group(control = self.control)
        return locals()
    last = property(**last())
    def ret():
        doc = "The value to return"
        def fget(self): return self[localsdict.IVALS][localsdict.RET_VAL]
        def fset(self, value): self[localsdict.IVALS][localsdict.RET_VAL] = value
        def fdel(self): self[localsdict.IVALS][localsdict.RET_VAL] = group(control = self.control)
        return locals()
    ret = property(**ret())
    def escape():
        doc = "Set to True when trying to break out."
        def fget(self): return self[localsdict.IVALS][localsdict.ESCAPE_VAL]
        def fset(self, value): self[localsdict.IVALS][localsdict.ESCAPE_VAL] = value
        def fdel(self): self[localsdict.IVALS][localsdict.ESCAPE_VAL] = group(control = self.control)
        return locals()
    escape = property(**escape())






















