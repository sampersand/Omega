from Group import group
from Objects import ufuncobj, nullobj
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

    def __bool__(self):
        return any(isinstance(v, nullobj) for v in self.values())

    def __getattr__(self, attr):
        # return super().__getattr__(attr) if attr not in self.ivalsdict else self[attr]
        if __debug__:
            assert attr in self.ivalsdict, attr #needs to me in it!
        return self[attr]
    def __str__(self):
        return '{' + ', '.join(repr(v) + ':' + str(self[v]) for v in self if not self[v].isnull()) + '}'

class lcls(dict):
    def __new__(self, control):
        return super().__new__(self)

    def __init__(self, control):
        super().__init__(dict())
        self.control = control
        x = _lclsivls()
        self._ivalstr = x.omp + 'ivals'
        self[self._ivalstr] = x #ivals
        del x

    def __iter__(self):
        for k in super().__iter__():
            if k is self._ivalstr:
                for a in self[k]:
                    yield a
            else:
                yield k
    def __str__(self):
        return '{' + ', '.join(repr(v) + ':' + str(self[v]) for v in self if not self[v].isnull()) + '}'

    def __repr__(self):
        #[:-1] is '}'
        r = super().__repr__()[:-1]
        if __debug__:
            assert r[-1] == '}' #should be..
        return super().__repr__()[:-1] + self.iv.omp +'ivals:' + repr(self.iv) + '}'

    def clear(self):
        r = super().clear()
        del self.iv
        assert 0,' when ??' #when
        return r

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

    def iv():
        doc = "The internal values"
        def fget(self):
            return super().__getitem__(self._ivalstr)
        def fset(self, value):
            self[self._ivalstr] = value
        def fdel(self):
            del self[self._ivalstr]
        return locals()
    iv = property(**iv())