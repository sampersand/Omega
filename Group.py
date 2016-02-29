import copy
import Control
from Objects import obj, nullobj
class group(list):

    def __new__(self, base = None, control = None, args = [], parens = ('', '')):
        return super().__new__(self, args)

    def __init__(self, base = None, control = None, args = [], parens = ('', '')):
        super().__init__(args)
        if __debug__:
            assert control != None, 'should be set from somewhere'
        self.control = control
        self.base = obj.frombase(base, self.control)
        self.parens = parens

    def newgroup(self, base = None, args = [], parens = ('', '')):
        return group(base, self.control, args, parens)

    def isnull(self):
        return not bool(self or not self.base.isnull() or self.parens[0] or self.parens[1])

    def isfinal(self):
        return len(self) == 0

    @property
    def basestr(self):
        """ the string of this base """
        return str(self.base)
        # return '' if self.base.isnull() else str(self.base)
    
    def _hasparens(self):
        return bool(self.parens[0] or self.parens[1])

    def __repr__(self):
        ret = 'group('
        if not self.base.isnull():
            ret += 'base = ' + repr(self.base)  + ', '
        if self:
            ret += 'args = ' + super().__repr__() + ', '
        if self._hasparens():
            ret += 'parens = ' + repr(self.parens)
        if not self._hasparens() and (not self.base.isnull() or self):
            ret = ret[:-2]
        return ret + ')'

    def __str__(self):
        if not self:
            return ''.join((str(self.parens[0]), self.basestr, str(self.parens[1])))
        if self.basestr in self.control.opers['binary']:
            if __debug__:
                assert len(self.parens) == 2, repr(self)
            return self.parens[0] + (' ' + self.basestr +' ').join(str(e) for e in self) + str(self.parens[1])
        return ''.join((self.basestr, str(self.parens[0]), ', '.join(str(x) for x in self), str(self.parens[1])))

    def __getitem__(self, item): #so i can slice stuff...
        if isinstance(item, slice):
            return group(base = self.base, control = self.control, args = super().__getitem__(item), parens = self.parens)
        return super().__getitem__(item)

    # def linestr(self):
    #     def _linestr(self, ret, indent):
    #         if not self:
    #             # ret.append((str(self), indent))
    #             return [str(self), indent]
    #         isendl = self.basestr in self.control.delims['endline'][0]
    #         q = []
    #         for l in self:
    #             if l.isnull():
    #                 continue
    #             x = _linestr(l, [], indent + isendl)
    #             if isinstance(x[0], str) and q:
    #                 q[-1][0] += self.basestr + x[0]
    #             else:
    #                 q.append(x)
    #             print(x)
    #         ret.__iadd__(q)
    #         return ret
    #     lines = _linestr(self, [], 0)
    #     ret = '\n'
    #     for line in range(len(lines)):
    #         l = lines[line]
    #         ret += '{:^3}|  {}{}\n'.format(line, '\t'*l[1], str(l[0]))
    #     return ret
    def linestr(self):
        def _linestr(self, ret, indent):
            if not self:
                # ret.append((str(self), indent))
                return (str(self), indent)
            isendl = self.basestr in self.control.delims['endline'][0]
            q = []
            for l in self:
                if l.isnull():
                    continue
                x = _linestr(l, [], indent + isendl)
                q.append(x)
            ret.__iadd__(q)
            return ret
        lines = _linestr(self, [], 0)
        ret = '\n'
        for line in range(len(lines)):
            l = lines[line]
            ret += '{:^3}|  {}{}\n'.format(line, '\t'*l[1], str(l[0]))
        return ret
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

    def eval(self, ldict):
        if self.basestr in ldict:
            ldict.last = ldict[self.basestr]
        elif not self.base.isnull():
            self.base.eval(self, ldict)
        else:
            assert 0, 'when does this happen?' + str(self)

    def deepcopy(self):
        return copy.deepcopy(self)

