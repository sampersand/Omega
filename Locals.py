from Group import group
from Objects import ufuncobj
class _lclsivls(dict):
    omp = '$' #om prefix
    ivalsdict = { #ivals dict
        'last' : omp,
        'ret'  : omp + 'ret',
        'esc'  : omp + 'esc',
    }
    _invivalsdict = {v: k for k, v in ivalsdict.items()}
    def __init__(self):
        super().__init__(dict())
        for iv in self.ivalsdict:
            self[iv] = group()

    def __getattr__(self, attr):
        return super().__getattr__(attr) if attr not in self.ivalsdict else self[attr]

    def __radd__(self, other):
        if not isinstance(other, lcls):
            return NotImplemented
        x = other.copy()
        x.update({self.ivalsdict[e]:self[e] for e in self if not self[e].isnull()})
        return x
class lcls(dict):
    def __new__(self, control):
        return super().__new__(self)

    def __init__(self, control):
        super().__init__(dict())
        self.control = control
        self.iv = _lclsivls() #ivals
        
    def __str__(self):
        return '{' + ', '.join(repr(v) + ' : ' + str(self[v]) for v in self + self.iv) + '}'
    def __repr__(self):
        return (self + self.iv).__repr__()
    def clear(self):
        del self.iv
        return super().clear()

    def onlyfuncs(self):
        ret = lcls(self.control)
        for e in self:
            if isinstance(self[e].base, ufuncobj):
                ret[e] = self[e]
        return ret

    def __getitem__(self, item):
        if item in self.iv._invivalsdict:
            return self.iv[self.iv._invivalsdict[item]]
        return super().__getitem__(item)