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
            assert eles.base is self
        locls.lv = eles

    def updatebase(self, name, other):
        if   name == '+' : self.base += other.base
        elif name == '-' : self.base -= other.base
        elif name == '%' : self.base %= other.base
        elif name == '/' : self.base /= other.base
        elif name == '*' : self.base *= other.base
        elif name == '**': self.base **= other.base
        elif name == 'b>': self.base >>= other.base
        elif name == 'b<': self.base <<= other.base
        elif name == 'b^': self.base ^= other.base
        elif name == 'b|': self.base |= other.base
        elif name == 'b&': self.base &= other.base2
        else: raise ValueError("Unkown operator '{}'".format(name))

    @staticmethod
    def comparebase(this, name, other):
        from group import group
        if __debug__:
            assert isinstance(this, group), this
            assert isinstance(other, group), other
        if   name == '<' :                 return group(boolobj(this.base.base <   other.base.base))
        elif name == '>' :                 return group(boolobj(this.base.base >   other.base.base))
        elif name == '<=':                 return group(boolobj(this.base.base <=  other.base.base))
        elif name == '>=':                 return group(boolobj(this.base.base >=  other.base.base))
        elif name == '==' or name == '=':  return group(boolobj(this.base.base ==  other.base.base))
        elif name == '!=' or name == '<>': return group(boolobj(this.base.base !=  other.base.base))
        elif name == 'or' or name == '||': return this or other #todo these
        elif name == 'and'or name == '&&': return this and other
        else: raise ValueError("Unkown comparator '{}'".format(name))

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
        if __debug__:
            assert func == None or hasattr(func, '__call__'), type(func)
        self.func = func

    def __repr__(self):
        return 'funcobj({},base={})'.format(self.func, self.base)

    def eval(self, eles, locls):
        import control
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
        else:
            import inbuiltfuncs
            return inbuiltfuncs.evalconsts(self, eles, locls)
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
        return 'operobj({},{})'.format(self.base, self.priority, self.func)

    def __ge__(self, other):
        return self.priority >= other.priority

    def eval(self, eles, locls):
        if __debug__:
            assert eles.base is self
            import control
            assert self.base in control.allopers, str(self) + " needs to be in control.allopers!"
            assert self.func == None, str(self) + " can't be in control.functions & have a function defined!"+\
                                                   "(supposed to be defined in inbuiltfuncs)"
        import inbuiltfuncs
        inbuiltfuncs.evaloper(self, eles, locls)

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
    intre = re.compile(r'[\d]+')
    @staticmethod
    def fromstr(base):
        if not intobj.intre.fullmatch(base):
            return None
        return intobj(int(base))

    def __repr__(self):
        return 'intobj(%s)' % self.base

class floatobj(numobj):
    import re
    floatre = re.compile(r'^$') #todo: these

    @staticmethod
    def fromstr(base):
        if not floatobj.floatre.fullmatch(base):
            return None
        return floatobj(float(base))

    def __repr__(self):
        return 'floatobj(%s)' % self.base

class complexobj(numobj):
    import re
    complexre = re.compile(r'^$') #todo: these

    @staticmethod
    def fromstr(base):
        if not complexobj.complexre.fullmatch(base):
            return None
        return complexobj(complex(base))

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

