class objgrp(list):
    def __new__(self, data = None, objtype = None, args = list(), control = None, parens = ('', '')):
        return super().__new__(self, args)
    def __init__(self, data = None, objtype = None, args = list(), control = None, parens = ('', '')):
        if __debug__:
            assert control != None, 'Cannot pass an empty control!'
            assert isinstance(data, (str, type(None))), repr(data)
            assert isinstance(args, list)
        self.data = data
        self.objtype = objtype
        self.args = args
        self.control = control
        self.parens = parens
    def __repr__(self):
        ret = 'objgrp('
        if self.data != None: ret += 'data=%r,' % self.data
        if self.objtype != None: ret += 'objtype=%r,' % self.objtype
        if self.args != []: ret += 'args=%r,' % self.args
        # if self.control != None: ret += 'control=%r,' % self.control
        if self.parens != ('', ''): ret += 'parens=%r,' % self.parens
        return (ret != 'objgrp(' and ret[:-1] or objgrp) + ')'
    def __str__(self):
        if not self:
            return ''.join((str(self.parens[0]), str(self.data), str(self.parens[1])))
        if str(self.data) in self.control.opers['binary']:
            if __debug__:
                assert len(self.parens) == 2, repr(self)
            return self.parens[0] + (' ' + str(self.data) +' ').join(str(e) for e in self) + str(self.parens[1])
        return ''.join((str(self.data), str(self.parens[0]), ', '.join(str(x) for x in self), str(self.parens[1])))

    def linestr(self):
        linep = []
        def _linestr(self, indent):
            if not self:
                return str(self)
            isendl = self.basestr in self.control.delims['endline'][0]
            if __debug__:
                assert self.basestr
            ret = []
            for l in self:
                if l.isnull():
                    continue
                if isendl:
                    linep.append([])
                linel = len(linep) 
                ls = _linestr(l, indent + 1)
                if isendl:
                    ret.append('\n{:^3}|  {}{}'.format(linel, '\t' * (indent), ls))
                else:
                    ret.append(ls)
            retu = self.parens[0] + ('' if isendl else ' ' + self.basestr + ' ').join(ret)
            if isendl and self.parens[1]:
                linep.append([])
                retu += '\n{:^3}|  {}'.format(len(linep), '\t' * (indent-2))
            retu += self.parens[1]
            return retu
        return _linestr(self, 0)

