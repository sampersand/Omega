from Group import group
from Objects import ufuncobj
import copy
class localsdict(dict):
    om_pref = '$' #om prefix
    om_vals = om_pref + 'ivals'
    last_val = om_pref + ''
    ret_val = om_pref + 'ret'
    esc_val = om_pref + 'esc'

    def __new__(self, control, useIvals = True):
        return super().__new__(self)

    def __init__(self, control, useIvals = True):
        super().__init__(dict())
        self.control = control
        if useIvals:
            self.resetivals()

    def resetivals(self):
        self[localsdict.om_vals] = localsdict(self.control, False)
        for val in (localsdict.last_val, localsdict.ret_val, localsdict.esc_val):
            self[localsdict.om_vals][val] = group(control = self.control)

    def __iter__(self):
        for i in super().__iter__():
            if isinstance(self[i], dict) or not self[i].isnull():
                yield i

    def __str__(self):
        return '{' + ', '.join(repr(v) + ' : ' + str(self[v]) for v in self) + '}'

    def clear(self):
        ret = super().clear()
        self.resetivals()
        return ret

    def onlyfuncs(self):
        ret = localsdict(self.control)
        for e in self:
            if not isinstance(self[e], dict) and isinstance(self[e].base, ufuncobj):
                ret[e] = self[e]
        return ret

    def deepcopy(self):
        return copy.deepcopy(self)

    def last():
        doc = "The last value evaluated"
        def fget(self):
            return self[localsdict.om_vals][localsdict.last_val]
        def fset(self, value):
            self[localsdict.om_vals][localsdict.last_val] = value
        def fdel(self):
            self[localsdict.om_vals][localsdict.last_val] = group(control = self.control)
        return locals()
    last = property(**last())

    # def ret():
    #     doc = "The value to return"
    #     def fget(self):
    #         return self[localsdict.om_vals][localsdict.ret_val]
    #     def fset(self, value):
    #         self[localsdict.om_vals][localsdict.ret_val] = value
    #     def fdel(self):
    #         self[localsdict.om_vals][localsdict.ret_val] = group(control = self.control)
    #     return locals()
    # ret = property(**ret())

    # def escape():
    #     doc = "Set to True when trying to break out."
    #     def fget(self):
    #         return self[localsdict.om_vals][localsdict.esc_val]
    #     def fset(self, value):
    #         self[localsdict.om_vals][localsdict.esc_val] = value
    #     def fdel(self):
    #         self[localsdict.om_vals][localsdict.esc_val] = group(control = self.control)
    #     return locals()
    # escape = property(**escape())
