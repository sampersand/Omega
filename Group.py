from Objects import nullobj, obj
class group(list):
    def __init__(self, data = None, pobj = obj, control = None, args = [], parens = ('', '')):
        super().__init__(args)
        self.data = data
        self.obj = pobj
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
    def isnull(self):
        return isinstance(self.obj, nullobj) 
    def linestr(self):
        linep = []
        def _linestr(self, indent):
            if not self:
                return str(self)
            isendl = str(self.data) in self.control.delims['endline'][0]
            if __debug__:
                assert str(self.data)
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
            retu = self.parens[0] + ('' if isendl else ' ' + str(self.data) + ' ').join(ret)
            if isendl and self.parens[1]:
                linep.append([])
                retu += '\n{:^3}|  {}'.format(len(linep), '\t' * (indent-2))
            retu += self.parens[1]
            return retu
        return _linestr(self, 0)