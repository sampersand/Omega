class group(list):
    def __new__(self, base = '', args = [], parens = ('','')):
        return super().__new__(self, args)

    def __init__(self, base = '', args = [], parens = ('','')):
        import control
        self.base = control._getomobj(str(base))
        super().__init__(args)
        self.parens = parens
        if __debug__:
            import omobj
            assert isinstance(self.base, omobj.omobj), type(self.base)
            assert type(args) == list, "Expected {} for 'args', not '{}'!".format(type(list), type(args))
            assert type(parens) == tuple, "Expected {} for 'parens', not '{}'!".format(type(tuple), type(parens))
            assert len(parens) == 2, "Parens needs to be '(Left Paren, Right Paren)'! not '{}'".format(parens)

    def hasparens(self):
        return bool(self.parens[0] or self.parens[1])

    @property
    def basestr(self):
        return str(self.base)

    def isfinal(self):
        return len(self) == 0
    def __repr__(self):
        ret = 'group('
        if self.base:
            ret += 'base = ' + repr(self.base) + ', '
        if self:
            ret += 'args = ' + super().__repr__() + ', '
        if self.hasparens():
            ret += 'parens = ' + repr(self.parens)
        if not self.hasparens() and (self.base or self):
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
    
    def eval(self, locls):
        import control
        if __debug__:
            assert self.basestr != None
        if self.basestr in locls: #short cut
            locls['$'] = locls[self.basestr]
        else:
            self.base.eval(self, locls)
