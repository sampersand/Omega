class omobj:
    def __init__(self, base, evalfunc = None):
        if __debug__:
            assert not isinstance(base, omobj), base
        # self.base =  base.base if isinstance(base, omobj) else omobj._getbase(base)
        self.base = omobj._getbase(base)
        self.evalfunc = evalfunc
    @staticmethod
    def fromstr(base):
        import control
        return control.allkeywords[base] if base in control.allkeywords else str(base)
    @staticmethod
    def _getbase(base):
        if not isinstance(base, str) or not (base or base.isalnum()):
            return base
        import control
        if base[0] in control.allquotes:
            if __debug__:
                assert base[-1] in control.allquotes
            return base
        else:
            try:
                return int(base)
            except ValueError:
                try:
                    return float(base)
                except ValueError:
                    try:
                        return complex(base)
                    except ValueError:
                        # return str(base)
                        return control.allkeywords[base] if base in control.allkeywords else str(base)

    def __str__(self):
        return str(self.base)

    def __repr__(self):
        return 'omobj({},evalfunc={})'.format(repr(self.base), repr(self.evalfunc))

    def __bool__(self):
        return bool(str(self))
    def __eq__(self, other):
        if __debug__:
            assert isinstance(other, omobj), repr(other)
            assert hasattr(other, 'base'), "{} :: {}".format(repr(other), type(other))
            assert hasattr(other, 'evalfunc'), "{} :: {}".format(repr(other), type(other))
        return self.base == other.base and self.evalfunc == other.evalfunc

    def eval(self, eles, locls):
        if str(self) in locls:
            return
        if self.evalfunc == None:
            if hasattr(self.base, '__getitem__'):
                if __debug__:
                    assert len(eles) == 0, 'only one index for the time being'
                eles.eval(locls)
                locls['$'] = self.base[locls['$']]
            else:
                locls['$'] = self.base
        else:
            self.evalfunc(eles, locls)

class oper(omobj):

    def __init__(self, base, priority, evalfunc):
        super().__init__(base, evalfunc)
        self.priority = priority

    def __repr__(self):
        return 'oper({},{},{})'.format(self.base, self.priority, self.evalfunc)

    def __str__(self):
        return self.base
    def __lt__(self, other):
        return self.priority < other.priority

    def eval(self, eles, locls):
        if self.evalfunc == None:
            self._specialoper(eles, locls)
        elif eles:
            eles[0].eval(locls)
            ret = locls['$']
            name = eles.basestr
            for ele in eles[1:]:
                ele.eval(locls)
                ret = self.evalfunc(ret, locls['$'])
            locls['$'] = ret# x = y

    def _specialoper(self, eles, locls):
        from group import group
        import control
        name = eles.basestr
        if name in control.alldelims:
            if name in control.delims['arraysep']:
                eles[0].eval(locls)
                ret = []
                name = eles.basestr
                for ele in eles:
                    ele.eval(locls)
                    ret.append(locls['$'])
                locls['$'] = group(base = ret)# x = y
                return
            else:
                raise SyntaxError("Special Operator '{}' isn't defined yet!".format(name))
        elif name == ':':
            if eles[0].basestr in locls:
                locls[eles[0].basestr].base.eval(eles[1], locls)
            else:
                eles[0].base.eval(eles[1:],locls)
        elif name == '||' or name == '&&':
            eles[0].eval(locls)
            element = locls['$']
            if name == '&&' and not element or name == '||' and element:
                return element
            eles[1].eval(locls)
        else:
            direc = name[0] == '<' and name[-1] == '-'
            if direc == 1:
                eles[1].eval(locls)
                value =locls['$']
                key = eles[0].basestr
            else:
                eles[0].eval(locls)
                value =locls['$']
                key = eles[1].basestr
                name = '<' + name[1:-1] + '-'
            if __debug__:
                assert name == '<-'  or\
                       name == '->'  or\
                       name == '<?-' or\
                       name == '-?>' or\
                       key in locls, "'{}' needs to be defined to perform '{}' on it!".format(key, name)
            if   name == '<-'  : locls[key] = value
            elif name == '<?-' : locls[key] = value if value else (locls[key] if key in locls else None)
            elif name == '<+-' : locls[key] += value
            elif name == '<--' : locls[key] -= value
            elif name == '<*-' : locls[key] *= value
            elif name == '</-' : locls[key] /= value
            elif name == '<**-': locls[key] **= value
            elif name == '<%-' : locls[key] %= value
            elif name == '<&-' : locls[key] &= value
            elif name == '<|-' : locls[key] |= value
            elif name == '<^-' : locls[key] ^= value
            elif name == '<<-' : locls[key] <<= value
            elif name == '<>-' : locls[key] >>= value
            if direc == 0: #swap the return value
                locls['$'] = locls[key]

class func(omobj):
    def __init__(self, base):
        super().__init__(base, None)
    def eval(self, eles, locls):
        import control
        if self.evalfunc != None:
            super().eval(eles, local)
        else:
            if 'disp' in str(self):
                sep = str(self) == 'displ' and '\n' or str(self) == 'dispc' and ', ' or ''
                if len(eles) == 0: #aka just 'disp;'
                    print(end=sep)
                else:
                    if __debug__:
                        assert len(eles) == 1
                    for element in eles:
                        element.eval(locls)
                        print(locls['$'], end = sep)
            elif str(self) == 'abort':
                if eles.isfinal() and str(eles.base) != str(control.funcs['abort']):
                    locls['$'] = eles
                elif str(eles.base) == str(control.funcs['abort']): 
                    #'$' not in locls:
                    locls['$'] = ''
                if __debug__:
                    assert '$' in locls
                quit('Aborting!' + (str(locls['$']) and " Message: '{}'".format(str(locls['$']))))
            elif str(self) == 'if':
                if __debug__:
                    assert len(eles) in (2, 3), 'can only have if:(cond):(if true)[:(if false)];'
                eles[0].eval(locls) # evaluates the condition
                if locls['$']:
                    eles[1].eval(locls)
                elif len(eles) == 3:
                    eles[2].eval(locls)
            elif str(self) == 'for':
                if __debug__:
                    assert len(eles) == 2, 'can only have for:(...):{ expression };'
                    assert len(eles[0]) == 3, 'can only have (initialize; condition; increment)'
                eles[0][0].eval(locls) # initializes the for loop the condition
                print(eles[0][0])
                while True:
                    eles[0][1].eval(locls) #check the conditoin
                    if not locls['$']:
                        break
                    eles[1].eval(locls) #increment
                    eles[0][2].eval(locls)
            else:
                raise SyntaxError("function '{}' isn't defined yet!".format(str(self)))
