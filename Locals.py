from Group import group
from Objects import userobj, nullobj
class _lclsivls(dict):
    omp = '$' #om prefix

    idict = {
        # the key is what will be used internally
        # the value is what the user would use to access it.
        'last' : omp, #using for storing the last value
        'ret'  : omp + 'ret', #used for storing the return value
        'esc'  : omp + 'esc', #used for escaping out of loops
        'this' : omp + 'this', #used for inside classes
    }

    _invidict = {v: k for k, v in idict.items()}

    def __init__(self, control):
        self.control = control
        super().__init__(dict())
        for iv in self.idict:
            self[iv] = group(control = self.control)

    def __bool__(self):
        return any(v for v in self.values())

    def __getattr__(self, attr):
        return super().__getattr__(attr) if attr not in self.idict\
            else self.__getitem__(attr)

    def __setattr__(self, attr, value):
        return super().__setattr__(attr, value) if attr not in self.idict\
            else self.__setitem__(attr, value)

    def __delattr__(self, attr):
        return super().__delattr__(attr) if attr not in self.idict\
            else self.__setitem__(attr, group(control = self.control))

    def __str__(self):
        return '{' + ', '.join(repr(k) + ': `' + str(v) + '`' for k, v in self.items() if v) + '}'

    def __repr__(self):
        return '{' + ', '.join(repr(k) + ': ' + repr(v) for k, v in self.items() if v) + '}'

    def copylast(self):
        self.last = self.last.deepcopy()
        return self.last

class lcls(dict):
    """ The keeper of all the variables that are being used. """

    def __new__(self, control):
        return super().__new__(self)

    def __init__(self, control):
        super().__init__(dict())
        self.control = control

        x = _lclsivls(self.control)
        self._ivalstr = x.omp + 'ivals'
        super().__setitem__(self._ivalstr, x) #ivals

        del x

    def __iter__(self):
        for k, v in self.items():
            if v is self.iv:
                for a in v._invidict:
                    yield a
            else:
                yield k

    def __getitem__(self, item):
        if item in self.iv._invidict:
            return self.iv[self.iv._invidict[item]]
        return super().__getitem__(item)

    def __contains__(self, item):
        return item in iter(self)

    def __setitem__(self, item, value):
        if item in self.iv._invidict:
            ret = self.iv.__setitem__(self.iv._invidict[item], value)
            if value is self.iv.last: #so we don't accidentally set the return value twice
                return ret
        else:
            ret = super().__setitem__(item, value)
        self.iv.last = value
        return ret

    def __delitem__(self, item):
        if item in self.iv._invidict:
            return self.iv.__delitem__(self.iv._invidict(item))
        return super().__delitem__(item)

    def __str__(self):
        return '{' + ', '.join(repr(k) + ': `' + str(self[k]) + '`' for k in self if bool(self[k])) + '}'

    def clear(self):
        r = super().clear()
        x = _lclsivls(self.control)
        self._ivalstr = x.omp + 'ivals'
        super().__setitem__(self._ivalstr, x) #ivals
        return r

    def onlyuobjs(self):
        ret = lcls(self.control)
        for e in self:
            if isinstance(self[e].baseobj, userobj) or e == self.iv.idict['this']:
                ret[e] = self[e]
        return ret

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





