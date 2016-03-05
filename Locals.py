from Group import group
from Objects import ufuncobj
import copy
class lclsivals(dict):
    omp = '$' #om prefix
    ivd = { #ivals dict
        'last' : omp,
        'ret'  : omp + 'ret',
        'esc'  : omp + 'esc',}

class lcls(dict):
    _ivalpref = lclsivals.omp + 'ivals'
    def __new__(self, control):
        return super().__new__(self)

    def __init__(self, control):
        super().__init__(dict())
        self.control = control
        if useIvals:
            self.resetivals()

    # def resetivals(self):
    #     self.ivals = lcls(self.control, False)
    #     for val in lcls.ivd.values():
    #         if val is not lcls.ivd['ivals']:
    #             self.ivals[val] = group(control = self.control)

    def __str__(self):
        return '{' + ', '.join(repr(v) + ' : ' + str(self[v]) for v in self + self.ivals) +  + '}'

    def clear(self):
        del self.ivals
        return super().clear()
        # ret = super().clear()
        # return ret

    def onlyfuncs(self):
        ret = lcls(self.control)
        for e in self:
            if isinstance(self[e].base, ufuncobj):
                ret[e] = self[e]
        return ret

    def deepcopy(self):
        return copy.deepcopy(self)

    # @property
    # def ivals(self):
    #     """ The internal values (used to keep track of things like return values) """
    #     return self._ivals

    # @ivals.deleter
    # def ivals(self):
    #     del self._ivals