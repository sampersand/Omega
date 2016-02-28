from group import group
class omobj:
    def __init__(self, base, evalfunc = None):
        if __debug__:
            assert not isinstance(base, omobj), base
        self.base = base
        self.evalfunc = evalfunc
    @staticmethod
    def genobj(base, evalfunc = None):
        if isinstance(base, omobj):
            if __debug__:
                assert evalfunc == None
            return base
        if not isinstance(base, str):
            if isinstance(base, list):
                if __debug__:
                    assert evalfunc == None
                return array(base)
            return omobj(base, evalfunc)
        import control
        if base in control.allkeywords:
            if __debug__:
                assert evalfunc == None
            return control.allkeywords[base]
        if not(base or base.isalnum()):
            return omobj(base, evalfunc)
        if base[0] in control.allquotes:
            if __debug__:
                assert base[-1] in control.allquotes
            return omobj(base, evalfunc)
        try:
            return omobj(eval(base), evalfunc)
        except SyntaxError:
            return omobj(str(base), evalfunc)
        except NameError:
            return omobj(str(base), evalfunc)

    def __str__(self):
        return str(self.base)

    def __repr__(self):
        return 'omobj(' + repr(self.base) + ('' if self.evalfunc == None else ', {}'.format(repr(self.evalfunc))) + ')'

    def __bool__(self):
        return bool(self.base)
        # return bool(str(self))

    def _func_eq(self, other):
        if __debug__:
            assert isinstance(other, omobj), repr(other)
            assert hasattr(other, 'base'), "{} :: {}".format(repr(other), type(other))
            assert hasattr(other, 'evalfunc'), "{} :: {}".format(repr(other), type(other))
        return self.base == other.base and self.evalfunc == other.evalfunc
    def eval(self, eles, locls):
        if str(self) in locls:
            # assert 0, 'when does this happen? ' + repr(self)
            if __debug__:
                assert len(locls[str(self.base)]) == 0, 'why doenst this work??'
            locls[str(self.base)].base.eval(eles, locls)
        if self.evalfunc == None:
            locls['$'] = self
        else:
            locls['$'] = self.evalfunc(eles, locls)
        assert isinstance(locls['$'], group), repr(locls['$'])
        return locls['$']

    def _updatebase(self, fname, value):
        if fname == '':
            self.base = value.base
        elif fname == '?':
            self.base = value.base or self.base
        elif fname == '+':
            self.base += value.base
        elif fname == '-':
            self.base -= value.base 
        elif fname == '*':
            self.base *= value.base 
        elif fname == '/':
            self.base /= value.base 
        elif fname == '**':
            self.base **= value.base 
        elif fname == '%':
            self.base %= value.base 
        elif fname == '&':
            self.base &= value.base 
        elif fname == '|':
            self.base |= value.base 
        elif fname == '^':
            self.base ^= value.base 
        elif fname == '<':
            self.base <<= value.base 
        elif fname == '>':
            self.base >>= value.base
        else:
            print('warning: function \'{}\' is not implemented yet!'.format(fname))
            return NotImplemented
        return self

    
    def _updateEles(self, eles, locls, direc):
        keystr = str(eles[direc])
        if __debug__:
            assert isinstance(eles[not direc], group), repr(eles[not direc])
        valueobj = eles[not direc].base.eval(eles, locls)
        if __debug__:
            assert isinstance(valueobj, group)
        if keystr not in locls:
            import copy
            locls[keystr] = copy.copy(valueobj) #oh boy this was giving issues...
        elif isinstance(locls[keystr], group): #used to be obj base
            locls[keystr]._updatebase(str(self)[1:-1], valueobj)
        locls['$'] = locls[keystr]

class oper(omobj):

    def __init__(self, base, priority, evalfunc = None):
        super().__init__(base, evalfunc)
        self.priority = priority

    def __repr__(self):
        return 'oper({},{},{})'.format(repr(self.base), repr(self.priority), repr(self.evalfunc))

    def __lt__(self, other):
        return self.priority < other.priority

    def eval(self, eles, locls):
        if self.evalfunc == None:
            locls['$'] = self._specialoper(eles, locls)
        else:
            if __debug__:
                assert eles, 'this shouldn"t break!'
            ret = eles[0].eval(locls)
            if __debug__:
                assert isinstance(ret, 1)
            name = eles.basestr
            for ele in eles[1:]:
                ret = gself.evalfunc(ret.base, ele.eval(locls).base)
            locls['$'] = ret #do i even need this
        return locls['$']

    def _specialoper(self, eles, locls):
        from group import group
        import control
        name = str(self)
        if __debug__:
            if str(self) != ';':
                assert 0, repr(self)
        if name in control.alldelims:
            if name in control.delims['arraysep'][0]:
                ret = []
                name = eles.basestr
                for ele in eles:
                    ret.append(group(base = ele).eval(locls))
                locls['$'] = group(base = ret)
            elif name in control.delims['endline'][0]:
                for ele in eles:
                    group(base = ele).eval(locls) #will set locls by itself
            else:
                raise SyntaxError("Special Operator '{}' isn't defined yet!".format(name))
        elif name == ':':
            # if __debug__:
                # assert not eles[0], eles[0] #just a thing i noticed, no hard and fast rule
            if __debug__:
                assert 0, 'come back'
            eles[0].base.eval(eles[1:],locls) #already set themselves to '$'
        elif name == '||' or name == '&&':
            typ = name == '&&'
            
            element = eles[0].eval(locls)
            if (typ and element) or (not typ and not element):
                return 99
            eles[1].eval(locls) #already set themselves to '$'
        else:
            if __debug__:
                assert len(eles) == 2
            direc = str(self)[0] == '-'
            if __debug__:
                 assert direc and name[-1] == '>' or not direc and name[0] == '<'
            self._updateEles(eles, locls, direc) #already sets itself to '$'
        return locls['$']

    def _updateEles(self, eles, locls, direc):
        if str(eles[direc].base) == ':':
            if __debug__:
                assert len(eles[direc]) == 2, 'currently, only \'array:[position]\''
                assert eles[direc][0].basestr in locls,'cannot perform operation on empty elements!'
                assert not len(locls[eles[direc][0].basestr]), 'uh, why did this happen?? ' + repr(eles)
                assert isinstance(locls[eles[direc][0].basestr].base, array), 'ATM, only can get elements from arrays!'
            valueobj = eles[not direc].eval(eles, locls)
            locls[eles[direc][0].basestr].base._updatebase(str(self)[1:-1], valueobj, eles[direc][1].eval(locls))
        if str(eles[not direc].base) == ':':
            # print(eles[not direc], type(eles[not direc]))
            eles[not direc] = eles[not direc].base.eval(eles, locls)
            return super()._updateEles(eles, locls, direc)
        else:
            return super()._updateEles(eles, locls, direc)
        # locls['$'] = locls[keystr]



        #eles[0].base.eval(eles[1:],locls) #already set themselves to '$'

class func(omobj):
    def __init__(self, base):
        super().__init__(base, None)
    
    def eval(self, eles, locls):
        import control
        if self.evalfunc != None:
            return super().eval(eles, local)
        else:
            if 'disp' in str(self.base):
                sep = str(self.base) == 'displ' and '\n' or str(self.base) == 'dispc' and ', ' or ''
                if len(eles) == 0: #aka just 'disp;'
                    print(end=sep)
                else:
                    if __debug__:
                        assert len(eles) == 1
                    for element in eles:
                        element.eval(locls) #yes ik this is still here
                        from group import group
                        if isinstance(locls['$'], group):
                            print(sep.join(str(e) for e in locls['$'].base.base), end = sep)
                        else:
                            print(locls['$'], end = sep)
            elif str(self.base) == 'abort':
                if eles.isfinal() and str(eles.base) != str(control.funcs['abort']):
                    locls['$'] = group(base = eles)
                elif str(eles.base) == str(control.funcs['abort']): 
                    locls['$'] = group(base = null())
                quit('Aborting!' + (str(locls['$']) and " Message: '{}'".format(str(locls['$']))))
            elif str(self) == 'if':
                if __debug__:
                    assert len(eles) in (2, 3), 'can only have if:(cond):(if true)[:(if false)];'
                 # evaluates the condition
                if eles[0].eval(locls):
                    eles[1].eval(locls) #already set themselves to '$'
                elif len(eles) == 3:
                    eles[2].eval(locls) #already set themselves to '$'
            elif str(self) == 'for':
                if __debug__:
                    assert len(eles) == 2, 'can only have for:(...):{ expression };'
                    assert len(eles[0]) == 3, 'can only have (initialize; condition; increment)'
                eles[0][0].eval(locls) # initializes the for loop the condition
                while True:
                    eles[0][1].eval(locls) #check the conditoin
                    if not locls['$']:
                        break
                    eles[1].eval(locls) #do the expression
                    eles[0][2].eval(locls) #increment
            elif str(self) == 'skip':
                if '$' not in locls:
                    locls['$'] = group(args = null())
            elif str(self) == 'del':
                if str(eles) == "'*'":
                    locls.clear()
                for ele in eles:
                    if str(ele) in locls:
                        del locls[str(ele)]
                if '$' not in locls:
                    locls['$'] = group(args = null())
            else:
                raise SyntaxError("function '{}' isn't defined yet!".format(str(self)))
        if __debug__:
            assert '$' in locls
        return locls['$']
class array(omobj):
    def __init__(self, base):
        super().__init__(base, None)


    def __repr__(self):
        return 'array({})'.format(repr(self.base))

    def eval(self, eles, locls):
        if hasattr(self.base, '__getitem__'):
            if __debug__:
                assert len(eles) == 1, 'only one index for the time being ' + repr(eles) + str(len(eles))
            group(base = eles[0]).eval(locls)
            locls['$'] = self.base[locls['$'].base]
        return locls['$']
    def _updatebase(self, fname, value, position = 0):
        if position.base >= len(self.base):
            import control
            self.base.extend(null() for x in range(position.base - len(self.base) + 1))
        if fname == '':
            self.base[position.base] = value
        else:
            self.base[position.base]._updatebase(fname, value)
        return self

class null(omobj):
    def __init__(self):
        super().__init__(None, None)
    def __repr__(self):
        return 'null()'
    def __str__(self):
        return 'null'
    def _func_eq(self, other):
        return isinstance(other, null)
    def __bool__(self):
        return False
    def _updatebase(self, fname, value):
        return value