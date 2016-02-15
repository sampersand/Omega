from control import control
class group(list):
    def __new__(self, val = '', args = [], parens = ('','')):
        return super().__new__(self, args)

    def __init__(self, val = '', args = [], parens = ('','')):
        super().__init__(args)
        if __debug__:
            assert type(val) == str, val
            assert type(args) == list, str(args) + str(type(args))
            assert type(parens) == tuple, str(parens) + str(type(parens))
            assert len(parens) == 2, parens
        self.val = val
        self.parens = parens
    def hasparens(self):
        return bool(self.parens[0] or self.parens[1])

    def __repr__(self):
        ret = 'group('
        if self.val:
            ret += 'val = ' + repr(self.val) + ', '
        if self:
            ret += 'args = ' + super().__repr__() + ', '
        if self.hasparens():
            ret += 'parens = ' + repr(self.parens)
        if not self.hasparens() and (self.val or self):
            ret = ret[:-2]
        return ret + ')'

    def __str__(self):
        if not self:
            return ''.join((str(self.parens[0]), str(self.val), str(self.parens[1])))
        if self.val in control.opers['binary']:
            if __debug__:
                assert len(self.parens) == 2, repr(self)
            return str(self.parens[0]) + str(self.val).join(str(e) for e in self) + str(self.parens[1])
        return ''.join((str(self.val), str(self.parens[0]), ', '.join(str(x) for x in self), str(self.parens[1])))
    def isempty(self):
        return self.isnull() or not self and not self.hasparens() and self.val in control.delims['endline'][0]
    def isnull(self):
        return not self and not self.hasparens() and not self.val
    def eval(self, locls):
        if self.isnull():
            locls['$'] = None
        elif self.val in control.allopers:
            control.evaloper(self, locls)
        elif self.val in control.funcs:
            control.funcs[self.val](self, locls)
        else:
            if self.val == '':
                if __debug__:
                    assert len(self) == 1, self #expects 1 element (in parens)
                self[0].eval(locls)
            elif self.val in locls:
                locls['$'] = locls[self.val]
            else:
                if self.val in control.consts:
                    locls['$'] = control.consts[self.val]
                else:
                    if self.val == 'locals' or self.val == 'locls':
                        locls['$'] = str(locls)
                    else:
                        if self.val[0] in control.allquotes:
                            if __debug__:
                                assert self.val[-1] in control.allquotes
                            locls['$'] = self.val
                        else:
                            try:
                                locls['$'] = int(self.val)
                            except ValueError:
                                try:
                                    locls['$'] = float(self.val)
                                except ValueError:
                                    try:
                                        locls['$'] = complex(self.val)
                                    except ValueError:
                                        raise SyntaxError('No known way to deal with \'{}\''.format(self.val))
