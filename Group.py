from Objects import nullobj, obj
class group(list):
    def __init__(self, data = None, pobj = None, control = None, args = [], parens = ('', '')):
        super().__init__(args)
        self.data = data
        self.obj = obj() if pobj == None else pobj
        self.control = control
        self.args = args
        self.parens = parens

    def __repr__(self):
        ret = 'objgrp('
        if self.data != None: ret += 'data={},'.format(repr(self.data))
        if self.obj != None: ret += 'obj={},'.format(repr(self.obj))
        if bool(self): ret += 'args={},'.format(super().__repr__())
        # if self.control != None: ret += 'control=%r,' % self.control
        if self.parens != ('', ''): ret += 'parens={},'.format(repr(self.parens))
        return (ret != 'objgrp(' and ret[:-1] or objgrp) + ')'

    def __str__(self):
        if not self:
            return ''.join((str(self.parens[0]), str(self.data), str(self.parens[1])))
        print(str(self.data))
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
            isendl = str(self.data) in self.control.delims['endline'][0]
            if __debug__:
                assert str(self.data)
            lines = []
            for l in self:
                if l.isnull():
                    continue
                if isendl:
                    linep.append([])
                linel = len(linep) 
                ls = _linestr(l, indent + 1)
                if isendl:
                    lines.append('\n{:^3}|  {}{}'.format(linel, '\t' * (indent), ls))
                else:
                    lines.append(ls)
            ret = self.parens[0] + ('' if isendl else ' ' + str(self.data) + ' ').join(lines)
            if isendl and self.parens[1]:
                linep.append([])
                ret += '\n{:^3}|  {}'.format(len(linep), '\t' * (indent-2))
            ret += self.parens[1]
            return ret
        return _linestr(self, 0)

    def isnull(self):
        """ cheks if this group's obj is null. """
        return isinstance(self.obj, nullobj) 


    def evaluate(self, ldict):
        return self.obj.evaluate(self)