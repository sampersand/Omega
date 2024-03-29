import re, copy
from Objects import nullobj, obj, arrayobj
from Objects import objregexes
class group(list):
    defaultparens = ('', '')

    _attrsdict = {'data' : '$__data', 'lcls' : '$__lcls', 'name' : '$__name'}

    def __init__(self, data = None, baseobj = None, control = None, args = [], parens = defaultparens,
                 attrs = None):
        super().__init__(args)
        self.attrs = {} if attrs == None else attrs
        self.attrs[self._attrsdict['data']] = data
        if __debug__:
            assert control != None, 'cannot have a None control!' + str(control)
        self.control = control
        self.parens = parens
        self.baseobj = self.getobj() if baseobj == None else baseobj

    def hasparens(self):
        return self.parens != self.defaultparens

    def __repr__(self):
        ret = 'group('
        if self.data != None:
            ret += 'data= {}, '.format(repr(self.data))
        if self.baseobj != nullobj:
            ret += 'baseobj= {}, '.format(repr(self.baseobj))
        if len(self):
            ret += 'args= {}, '.format(super().__repr__())
        if self.hasparens():
            ret += 'parens= {}, '.format(repr(self.parens))
        if len(self.attrs.keys()) != 1:
            ret += 'attrs= {}, '.format(repr(self.attrsnodata))
        return (ret != 'group(' and ret[:-2] or ret) + ')'

    @property
    def attrsnodata(self):
        return {x:self.attrs[x] for x in self.attrs if x != self._attrsdict['data']}

    # def __str1__(self):
    #     return self.__str1__() + \
    #         (len(self.attrs.keys()) != 1 and str({x:str(self.attrs[x]) for x in self.attrsnodata}) or '')

    def __str__(self):
        return self.baseobj.groupstr(self)

    def __bool__(self):
        """ False if this thing's baseobj is a nullobj. """
        return not isinstance(self.baseobj, nullobj) or self.baseobj.isuser

    def __getitem__(self, item):
        if isinstance(item, slice):
            return group(data = self.data,
                         baseobj = self.baseobj,
                         control = self.control,
                         args = super().__getitem__(item),
                         parens = self.parens,)
        return super().__getitem__(item)

    def __contains__(self, other):
        """ checks to see if the other's data is one of this group's arg's data"""
        if isinstance(other, group):
            other = other.data
        for arg in self:
            if arg.data == other:
                return True
        return False

    def linestr(self):
        class _int():
            def __init__(self):
                self.pos = 0
            def __iadd__(self, other):
                self.pos += other
            def __int__(self):
                return self.pos
        linep = _int()
        def _linestr(self, indent):
            if not len(self):# or self.data and len(self):
                # print(self.data)
            # if not self.data or not len(self):
                return str(self)
            isendl = self.datastr in self.control.delims['endline'][0]
            lines = []
            for l in self:
                if not l:
                    continue
                if isendl:
                    linep.__iadd__(1)
                ls = _linestr(l, indent + 1)
                if isendl:
                    lines.append('\n{:^3}|  {}{}'.format(int(linep), '\t' * (indent), ls))
                else:
                    lines.append(ls)
            ret = self.parens[0] + ('' if isendl else ' ' + self.datastr + ' ').join(lines)
            if isendl and self.parens[1]:
                linep.__iadd__(1)
                ret += '\n{:^3}|  {}'.format(int(linep), '\t' * (indent-2))
            ret += self.parens[1]
            return ret
        return _linestr(self, 0)

     # def linestr(self):
     #    def _linestr(self, ret, indent):
     #        if not self:
     #            # ret.append((str(self), indent))
     #            return (str(self), indent)
     #        isendl = self.datastr in self.control.delims['endline'][0]
     #        q = []
     #        for l in self:
     #            if l.isnull():
     #                continue
     #            x = _linestr(l, [], indent + isendl)
     #            q.append(x)
     #        ret.__iadd__(q)
     #        return ret
     #    lines = _linestr(self, [], 0)
     #    ret = '\n'
     #    for line in range(len(lines)):
     #        l = lines[line]
     #        ret += '{:^3}|  {}{}\n'.format(line, '\t'*l[1], str(l[0]))
     #    return ret

    def getobj(self):
        if self.data == None and self.hasparens():
            return arrayobj()
        if self.data == None:
            return nullobj()
        if __debug__:
            assert isinstance(self.data, str), "'%s' has to be of type str, not '%s'" %(self.data, type(self.data))
        for key in objregexes:
            m = re.fullmatch(key.format(quote = self.control.allquotes, escape = self.control.escape), self.datastr)
            if m:
                self.data = m.groupdict()['keep']
                if objregexes[key] == nullobj:
                    return objregexes[key](isuser = True)
                return objregexes[key]()
        if self.data in self.control.allkws:
            return self.control.allkws[self.data]
        return obj()

    def evalgrp(self, lcls):
        return self.baseobj.evalobj(self, lcls)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        return group(data = copy.deepcopy(self.data, memo),
                     baseobj = copy.deepcopy(self.baseobj, memo),
                     control = self.control,
                     args = copy.deepcopy(list(self), memo),
                     attrs = copy.deepcopy(self.attrs, memo),
                     parens = copy.deepcopy(self.parens, memo))

    @property
    def datastr(self):
        return '' if self.data == None else str(self.data)

    # 4/22 NOTE: I removed the only calling site of this, but with all the meta-
    # programming I was wary removing it. So here it shall stay.
    def updatedata(self, datagroup, funcname):
        self.data = datagroup.data

    def scrubstr(self, control):
    # def scrubstr(self, control, **kwargs):
        # print(str(self), kwargs, sep = '\t|\t')

        ret = str(self)
        # ret = str(self).format(**kwargs)
        if ret and ret[0] in self.control.allquotes:
            if __debug__:
                assert ret[-1] in self.control.allquotes #can't have unmatched quotes
            ret = ret[1:-1]
        for k, v in control.escapechars.items():
            ret = ret.replace(k, v)
        return ret

    def clear(self):
        super().clear()
        self.data = None
        self.parens = self.defaultparens
        self.baseobj = self.getobj()

    def data():
        doc = "The data that this group contains"
        def fget(self):
            return self.attrs[self._attrsdict['data']]
        def fset(self, value):
            self.attrs[self._attrsdict['data']] = value
        return locals()
    data = property(**data())