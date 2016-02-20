from obj import *
class group(list):
    def __new__(self, base = None, args = [], parens = ('', '')):
        return super().__new__(self, args)
    def __init__(self, base = None, args = [], parens = ('', '')):
        super().__init__(args)
        self.base = obj.frombase(base)
        self.parens = parens

    def isempty(self):
        return bool(self or self.args or self.parens[0] or self.parens[1])

    def isfinal(self):
        return len(self) == 0

    @property
    def basestr(self):
        return '' if isinstance(self.base, nullobj) else str(self.base)
    
    def _hasparens(self):
        return bool(self.parens[0] or self.parens[1])

    # @property
    # def basestr(self):
    #     return str(self.base)

    # def isfinal(self):
    #     return len(self) == 0
        
    def __repr__(self):
        ret = 'group('
        if self.base:
            ret += 'base = ' + repr(self.base) + ', '
        if self:
            ret += 'args = ' + super().__repr__() + ', '
        if self._hasparens():
            ret += 'parens = ' + repr(self.parens)
        if not self._hasparens() and (self.base or self):
            ret = ret[:-2]
        return ret + ')'

    def __str__(self):
        import control
        if not self:
            return ''.join((str(self.parens[0]), self.basestr, str(self.parens[1])))
        if self.basestr in control.opers['binary']:
            if __debug__:
                assert len(self.parens) == 2, repr(self)
            return self.parens[0] + (self.basestr).join(str(e) for e in self) + str(self.parens[1])
        return ''.join((self.basestr, str(self.parens[0]), ', '.join(str(x) for x in self), str(self.parens[1])))

    def __getitem__(self, item):
        if isinstance(item, slice):
            return group(base = self.base, args = super().__getitem__(item), parens = self.parens)
        return super().__getitem__(item)

    def eval(self, locls):
        if self.basestr in locls: #short cut
            if __debug__:
                print("I'm in locls. Why exactly? ::",  self.basestr, repr(locls[self.basestr]))
            locls['$'] = locls[self.basestr]
        else:
            locls['$'] = self.base.eval(self, locls)
        if __debug__:
            assert isinstance(locls['$'], group)
        return locls['$']
