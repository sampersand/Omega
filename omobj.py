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
        # import control
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

    def __eq__(self, other):
        if __debug__:
            assert isinstance(other, omobj), repr(other)
            assert hasattr(other, 'base'), "{} :: {}".format(repr(other), type(other))
            assert hasattr(other, 'evalfunc'), "{} :: {}".format(repr(other), type(other))
        return self.base == other.base and self.evalfunc == other.evalfunc
    def eval(self, eles, locls):
        if str(self) in locls:
            assert 0, 'when does this happen?'
            locls[str(self.base)].eval(eles, locls)
        if self.evalfunc == None:
            locls['$'] = self
        else:
            self.evalfunc(eles, locls)
    # def __hash__(self):
    #     return hash(self.base) * hash(self.evalfunc)
    def update(self, value, fname):
        if fname == '':
            self.base = value.base
        elif fname == '?':
            assert 0, 'todo'
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
        # if __debug__:
        #     assert str(self) not in locls
        # if vals.isfinal():
        #     other.eval(locls)
        #     locls[str(self)] = locls['$']
        # else:
        # assert 0, repr(vals)

        # if __debug__:
            # assert not fname or fname == '?' or key in locls, "'{}'  exist, so cant do '{}'!".format(key, fname)
        # key.set(fname, fname, locls)
        # if direc == 0: #swap the return value
            # locls['$'] = locls[key]












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
            self._specialoper(eles, locls)
        else:
            if __debug__:
                assert eles, 'this shouldn"t break!'
            eles[0].eval(locls)
            ret = locls['$']
            name = eles.basestr
            for ele in eles[1:]:
                ele.eval(locls)
                print(ret,locls,eles,locls['$'].base)
                ret = omobj(self.evalfunc(ret.base, locls['$'].base))
                locls['$'] = ret
            locls['$'] = ret

    def _specialoper(self, eles, locls):
        from group import group
        import control
        name = str(self)
        if name in control.alldelims:
            if name in control.delims['arraysep'][0]:
                eles[0].eval(locls)
                ret = []
                name = eles.basestr
                for ele in eles:
                    ele.eval(locls)
                    ret.append(locls['$'])
                locls['$'] = group(base = ret)# x = y
                return
            if name in control.delims['endline'][0]:
                # if __debug__:
                    # assert len(eles) == 1, 'there should only be one! in \'{}\''.format(eles)
                for ele in eles:
                    ele.eval(locls)
            else:
                raise SyntaxError("Special Operator '{}' isn't defined yet!".format(name))
        elif name == ':':
            if __debug__:
                assert not eles[0] #just a thing i noticed, no hard and fast rule
            eles[0].base.eval(eles[1:],locls)
        elif name == '||' or name == '&&':
            typ = name == '&&'
            eles[0].eval(locls)
            element = locls['$']
            if (typ and element) or (not typ and not element):
                return
            eles[1].eval(locls)
        else:
            if __debug__:
                assert len(eles) == 2
            direc = name[0] == '-' and name[-1] == '>'
            keystr = str(eles[direc])
            eles[not direc].eval(locls)
            valueobj = locls['$']
            if name[1:-1] == '':
                locls[keystr] = valueobj
            else:
                if __debug__:
                    assert keystr in locls, 'cant update a non-existant object!'
                locls[keystr].update(valueobj, name[1:-1])
            locls['$'] = locls[keystr]
            # assert 0, '{} | {} | {} | {}'.format(repr(eles),repr(eles[direc]), locls, key)
            # key.set(name[1:-1], value)
            # locls['$'] = key.set(name[1:-1], value, locls)
            # if str(key) not in locls:
                # locls[str(key)] = locls['$']
            print(self,eles,locls,keystr,valueobj,sep="\t|\t")
class func(omobj):
    def __init__(self, base):
        super().__init__(base, None)
    
    def eval(self, eles, locls):
        # assert 0, 'todo: this'
        import control
        if self.evalfunc != None:
            super().eval(eles, local)
        else:
            if 'disp' in str(self.base):
                sep = str(self.base) == 'displ' and '\n' or str(self.base) == 'dispc' and ', ' or ''
                if len(eles) == 0: #aka just 'disp;'
                    print(end=sep)
                else:
                    if __debug__:
                        assert len(eles) == 1
                    for element in eles:
                        element.eval(locls)
                        from group import group
                        if isinstance(locls['$'], group):
                            print(sep.join(str(e) for e in locls['$'].base.base), end = sep)
                        else:
                            print(locls['$'], end = sep)
            elif str(self.base) == 'abort':
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
                print(eles[0][0],"@",locls)
                while True:
                    eles[0][1].eval(locls) #check the conditoin
                    print(locls['$'],'@',eles[0][1])
                    if not locls['$']:
                        break
                    eles[1].eval(locls) #increment
                    eles[0][2].eval(locls)
            else:
                raise SyntaxError("function '{}' isn't defined yet!".format(str(self)))

class array(omobj):
    def __init__(self, base):
        super().__init__(base, None)


    def __repr__(self):
        return 'array({})'.format(repr(self.base))

    def eval(self, eles, locls):
        if hasattr(self.base, '__getitem__'):
            if __debug__:
                assert len(eles) == 1, 'only one index for the time being'
            eles[0].eval(locls)
            # print(locls['$'])
            locls['$'] = self.base[locls['$']]






