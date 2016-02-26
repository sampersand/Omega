class group(list):
    def __new__(self, base = None, control = None, args = [], parens = ('', '')):
        return super().__new__(self, args)
    def __init__(self, base = None, control = None, args = [], parens = ('', '')):
        super().__init__(args)
        from Obj import obj
        if control == None:
            import Control
            control = Control.control()
        self.control = control
        self.base = obj.frombase(base, self.control)
        self.parens = parens

    def isempty(self):
        return not bool(self or not self.base.isnull() or self.parens[0] or self.parens[1])

    def isfinal(self):
        return len(self) == 0

    @property
    def basestr(self):
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
            return group(base = self.base, args = super().__getitem__(item), parens = self.parens)
        return super().__getitem__(item)

    # def linestr(self):
    #     def _linestr(self, ret, indent):
    #         if not self:
    #             # ret.append((str(self), indent))
    #             return [str(self), indent]
    #         isendl = self.basestr in self.control.delims['endline'][0]
    #         q = []
    #         for l in self:
    #             if l.isempty():
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
                if l.isempty():
                    continue
                x = _linestr(l, [], indent + isendl)
                q.append(x)
                print(x)
            ret.__iadd__(q)
            return ret
        lines = _linestr(self, [], 0)
        ret = '\n'
        for line in range(len(lines)):
            l = lines[line]
            ret += '{:^3}|  {}{}\n'.format(line, '\t'*l[1], str(l[0]))
        return ret
    def linestr(self):
        def _linestr(self, indent, linep):
            if not self:
                return str(self)
            isendl = self.basestr in self.control.delims['endline'][0]
            if __debug__:
                assert self.basestr
            ret = []
            for l in self:
                if l.isempty():
                    continue
                if isendl:
                    linep.append([])
                ls = _linestr(l, indent + 1, linep)
                if isendl:
                    ret.append('\n{:^3}|  {}{}'.format(len(linep), '\t' * (indent), ls))
                    # linep += 1
                else:
                    ret.append(ls)
            retu = self.parens[0] + ('' if isendl else ' ' + self.basestr + ' ').join(ret)
            if isendl and self.parens[1]:
                linep.append([])
                retu += '\n{:^3}|  {}'.format(len(linep), '\t' * (indent-2))
            retu += self.parens[1]
            return retu
        return _linestr(self, 0, [])





















