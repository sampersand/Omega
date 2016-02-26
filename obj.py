class obj():
    """
    The base class for all of the objects.
    """
    import re
    numre = re.compile(r'^(0[oxbOXB])?[\d.]+([eE]?[-+]?[\d.]+)?[ij]?$')

    def __init__(self, base):
        if __debug__:
            assert not isinstance(base, obj), type(obj) #only allowed to pass non-objs
        self.base = base

    @staticmethod
    def frombase(ele):
        """
        Used when passing a string to determine which base to use.
        """
        if isinstance(ele, obj):
            return ele
        if ele == None:
            return nullobj()
        if __debug__:
            assert isinstance(ele, str), type(ele) #can only read strs. otherwise, use appropriate subclass.
        import control
        if ele in control.allkeywords:
            return control.allkeywords[ele]
        ret = numobj.fromstr(ele)
        if ret == None:
            ret = strobj.fromstr(ele)
            if ret == None:
                ret = obj(ele)
                # raise ValueError("Don't know how to deal with base '{}'!".format(ele))            
        if __debug__:
            assert ret != None
        return ret

    def __str__(self):
        return str(self.base)

    @property
    def strobj(self):
        return strobj(str(self))

    def __repr__(self):
        return 'obj({})'.format(self.base)

    def __eq__(self, other):
        return isinstance(other, obj) and self.base == other.base

    def __bool__(self):
        return bool(self.base)

    def eval(self, eles, locls):
        if str(self) in locls:
            #this is ignoring the parens...
            locls[str(self)].base.eval(eles, locls)
            return
        if __debug__:
            assert eles.base is self, repr(eles) + " != " + repr(self)
        locls.lv = eles

    def updatebase(self, name, other):
        if   name == '+' : self.base += other.base
        elif name == '-' : self.base -= other.base
        elif name == '%' : self.base %= other.base
        elif name == '/' : self.base /= other.base
        elif name == '*' : self.base *= other.base
        elif name == '**': self.base **= other.base
        elif name == 'b>>': self.base >>= other.base
        elif name == 'b<<': self.base <<= other.base
        elif name == 'b^': self.base ^= other.base
        elif name == 'b|': self.base |= other.base
        elif name == 'b&': self.base &= other.base
        else: raise ValueError("Unnkown operator '{}'".format(name))

    @staticmethod
    def comparebase(this, name, other):
        from group import group
        if __debug__:
            assert isinstance(this, group), this
            assert isinstance(other, group), other
        if   name == '<' :                 return group(base = boolobj(this.base.base <   other.base.base))
        elif name == '>' :                 return group(base = boolobj(this.base.base >   other.base.base))
        elif name == '<=':                 return group(base = boolobj(this.base.base <=  other.base.base))
        elif name == '>=':                 return group(base = boolobj(this.base.base >=  other.base.base))
        elif name == '==' or name == '=':  return group(base = boolobj(this.base.base ==  other.base.base))
        elif name == '!=' or name == '<>': return group(base = boolobj(this.base.base !=  other.base.base))
        elif name == 'or' or name == '||': return this or other #todo these
        elif name == 'and'or name == '&&': return this and other
        else: raise ValueError("Unnkown comparator '{}'".format(name))

    def isnull(self):
        return isinstance(self, nullobj)

class funcobj(obj):
    """
    The class that represents a function.
    """
    def __init__(self, base, func = None):
        if func == None:
            func = None #yes, it looks stupid, but it's here so it cant get overrided later
        super().__init__(base)
        # if __debug__:
            # assert func == None or hasattr(func, '__call__'), type(func)
        self.func = func

    def __repr__(self):
        return 'funcobj({},base={})'.format(self.func, self.base)

    def eval(self, eles, locls):
        import control

        if eles.base is self:
            locls.lv = eles
            return
        if self.base in control.funcs:
            if __debug__:
                assert self.func == None, str(self) + " can't be in control.functions & have a function defined!"+\
                                                       "(supposed to be defined in inbuiltfuncs)"
            import inbuiltfuncs
            return inbuiltfuncs.evalfunc(self, eles, locls)
        if __debug__:
            x = locls.lv
        if self.func != None:
            self.func(eles, locls)
        if __debug__:
            assert locls.lv is not x, "function {} didn't do anything!".format(self)
class operobj(funcobj):
    """
    The class that represents operators on objects.
    """
    def __init__(self, base, priority):
        super().__init__(base, None)
        self.priority = priority

    def __repr__(self):
        return 'operobj({},{})'.format(self.base, self.priority)

    def __ge__(self, other):
        return self.priority >= other.priority

    def eval(self, eles, locls):
        if __debug__:
            assert eles.base is self, repr(eles) + ' != ' + repr(self)
            import control
            assert self.base in control.allopers, str(self) + " needs to be in control.allopers!"
            assert self.func == None, str(self) + " can't be in control.functions & have a function defined!"+\
                                                   "(supposed to be defined in inbuiltfuncs)"
        import inbuiltfuncs
        inbuiltfuncs.evaloper(self, eles, locls)
class userfuncobj(funcobj):
    def __init__(self, base, args, func):
        super().__init__(base, func)
        self.args = args

    def __repr__(self):
        return 'userfuncobj({},{},{})'.format(self.base, self.args, self.func)

    def _genargs(self, eles, locls):
        import locls as loclsm
        ret = loclsm.locls()
        # if __debug__:
        #     assert len(eles) == len(self.args), "{} args are required for '{}', got {} {}!".\
        #             format(len(self.args), self.base, len(eles), str(eles)[1:])
        for elep in range(len(self.args)):
            eles[elep].eval(locls)
            ret[str(self.args[elep])] = locls.lv
        return ret
    def eval(self, eles, locls):
        if __debug__:
            import control
            assert eles.basestr in control.delims['applier'][0] #f :(args) <-- needs the ':'
        if eles.base is self:
            locls.lv = eles
            return
        nlocls = self._genargs(eles[0], locls)
        self.func.eval(nlocls)
        if not nlocls.ret.base.isnull():
            locls.lv = nlocls.ret

class nullobj(obj):
    """
    The class that represents a null object.
    In reality, it is representing a 'None' object type, but there is no way to access 'None'.
    """
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return 'nullobj()'
        
    def __str__(self):
        return 'null'

    def eval(self, eles, locls):
        pass #do not change this

class strobj(obj):
    """
    The class that represents a string.
    """
    import re
    import control
    strre = re.compile(r'(?s)\A([{}]).*\1\Z'.format(control.allquotes))

    def __init__(self, base = None):
        if base == None:
            base = ''
        if __debug__:
            assert isinstance(base, str), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'strobj({})'.format(self.base)

    @staticmethod
    def fromstr(base):
        if not strobj.strre.fullmatch(base):
            return None
        return strobj(base)

    def scrub(self):
        import control
        base = self.base
        for c in control.escapechars:
            base = base.replace(c, control.escapechars[c])
        if base and base[0] in control.allquotes:  base = base[1:]
        if base and base[-1] in control.allquotes: base = base[:-1]
        return base

class arrayobj(obj):
    """
    The class that represents an array.
    """
    def __init__(self, base = None):
        if base == None:
            base = []
        if __debug__:
            assert isinstance(base, list), type(base) #atm, no tuples or sets or whatnot
        super().__init__(base)

    def __repr__(self):
        return 'arrayobj({})'.format(self.base)

    def __str__(self):
        return '[' + ', '.join(str(e) for e in self.base) + ']'

    def eval(self, eles, locls):
        if eles.base is self:
            locls.lv = eles
            return
        import inbuiltfuncs
        inbuiltfuncs.evalarray(self, eles, locls)

    @property
    def lenobj(self):
        return numobj(len(self.base))
class dictobj(obj):
    def __init__(self, base = None):
        if base == None:
            base = {}
        if __debug__:
            assert isinstance(base, dict), type(base)
        super().__init__(base)
    def __repr__(self):
        return 'dictobj({})'.format(self.base)

class numobj(obj):
    """
    The super class for all numbers.
    """

    TYPES = (int, float, complex)
    def __init__(self, base = None):
        if base == None:
            base = 0
        if __debug__:
            assert isinstance(base, numobj.TYPES), repr(base)
        super().__init__(base)

    def __repr__(self):
        return 'numobj({})'.format(self.base)

    @staticmethod
    def fromstr(base):
        ret = intobj.fromstr(base)
        if ret == None:
            ret = floatobj.fromstr(base)
            if ret == None:
                ret = complexobj.fromstr(base)
        return ret
class intobj(numobj):
    import re
    decre = re.compile(r'^(?:0([dD]))?(\d+)I?$') #can have 'I' at the end
    binre = re.compile(r'^0([bB])([01]+)I?$') #can have 'I' at the end
    hexre = re.compile(r'^0([xX])([\dA-Fa-f]+)I?$') #can have 'I' at the end
    octre = re.compile(r'^0([oO])([0-7]+)I?$') #can have 'I' at the end
    unire = re.compile(r'^0[uU](\d+)[uU](\d+)I?$') #can have 'I' at the end

    nbases = {'d':10, '':10, 'b':2, 'x':16, 'o':8}
    def __init__(self, base = 0, nbase = 10):
        if __debug__:
            assert isinstance(nbase, int) #needs to be!
        if isinstance(base, str):
            base = int(base, nbase)
        self.nbase = nbase
        super().__init__(base)
    @staticmethod
    def fromstr(base):
        ret = intobj.decre.findall(base)
        if not ret:
            ret = intobj.binre.findall(base)
            if not ret:
                ret = intobj.hexre.findall(base)
                if not ret:
                    ret = intobj.octre.findall(base)
        if ret:
            ret = (intobj.nbases[ret[0][0].lower()], ret[0][1])
        if not ret:
            ret = intobj.unire.findall(base)
            if ret:
                ret = (int(ret[0][0]), ret[0][1])
        if __debug__:
            assert not ret or len(ret) == 2 #only 1 or 0 matches
        return intobj(ret[1], ret[0]) if ret else None 

    def __repr__(self):
        return 'intobj(base={}{})'.format(self.base, '' if self.nbase == 10 else ',nbase='+str(self.nbase))

    #TODO: SSTRING FOR THIS
class floatobj(numobj):
    import re
    floatre = re.compile(r'^(\d*\.?\d+)(?:[eE]([nNpP]?)(\d+))?F?$') #float can have fF at the end

    @staticmethod
    def fromstr(base):
        ret = floatobj.floatre.findall(base)
        if ret:
            if __debug__:
                assert len(ret) == 1 #there should onyl be 1 match!
                assert len(ret[0]) == 3 #should be (###)e(pos/neg)(###)
            ret = ret[0]
            ret = (ret[2] and '{}e{}{}'.format(ret[0], ret[1] in 'pP' and '+' or '-', ret[2]) or ret[0])
            # for some reason, '' in 'pP' is true.
        return floatobj(float(ret)) if ret else None

    def __repr__(self):
        return 'floatobj(%s)' % self.base
    def eval(self, eles, locls):
        if eles.base is self:
            locls.lv = eles
            return
        import control
        if eles.basestr not in control.delims['applier'][0]:
            super().eval(eles, locls)
            return
        name = str(eles[0])
        if name == 'round':
            from group import group
            locls.lv = group(base = intobj(round(self.base)))
        else:
            raise SyntaxError("Unknown int function '{}'!".format(name))

class complexobj(numobj):
    import re
    complexre = re.compile(floatobj.floatre.pattern[:-1] + r'[iIjJ]$') #the exact same as a float with an I/J at the end

    @staticmethod
    def fromstr(base):
        ret = complexobj.complexre.findall(base)
        if ret:
            if __debug__:
                assert len(ret) == 1 #there should onyl be 1 match!
                assert len(ret[0]) == 3 #should be (###)e(pos/neg)(###)
            ret = ret[0]
            ret = (ret[2] and '{}e{}{}'.format(ret[0], ret[1] in 'pP' and '+' or '-', ret[2]) or ret[0])
            # for some reason, '' in 'pP' is true.
        return floatobj(complex(0, float(ret))) if ret else None

    def __repr__(self):
        return 'complexobj(%s)' % self.base
class boolobj(numobj):
    """
    The class that represents a boolean.
    """
    def __init__(self, base = None):
        if base == None:
            base = False
        if __debug__:
            assert isinstance(base, bool), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'boolobj({})'.format(self.base)














