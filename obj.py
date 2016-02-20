class obj():
    """
    The base class for all of the objects.
    """
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
        if ele in control.allfuncs:
            return control.allfuncs[ele]
        import re
        if re.fullmatch(control.numre, ele):
            return numobj.fromstr(ele)
        return obj(ele)

    def __str__(self):
        return str(self.base)

    def __repr__(self):
        return 'obj({})'.format(self.base)

    def __eq__(self, other):
        return isinstance(other, obj) and self.base == other.base

    def __bool__(self):
        return bool(self.base)

    def eval(self, eles, locls):
        if __debug__:
            assert eles.base is self
        locls['$'] = eles

    def dofunc(self, name, other):
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
        elif name == 'b&': self.base &= other.base
        else: raise ValueError("Unkown operator '{}'".format(name))
        return self

class funcobj(obj):
    """
    The class that represents a function.
    """
    def __init__(self, base, func = None):
        super().__init__(base)
        if __debug__:
            assert func == None or hasattr(func, '__call__'), type(func)
        self.func = func

    def __repr__(self):
        return 'funcobj({},base={})'.format(self.func, self.base)

    def eval(self, eles, locls):
        if __debug__:
            assert eles.base is self
        import control
        if self.base in control.funcs:
            if __debug__:
                assert self.func == None, str(self) + " can't be in control.functions & have a function defined! \
(supposed to be defined in inbuiltfuncs)"
            import inbuiltfuncs
            return inbuiltfuncs.evalfunc(self, eles, locls)
        if __debug__:
            x = locls['$']
        self.func(eles, locls)
        if __debug__:
            assert locls['$'] is not x, "function {} didn't do anything!".format(self)

class operobj(funcobj):
    """
    The class that represents operators on objects.
    """
    def __init__(self, base, priority):
        super().__init__(base, None)
        self.priority = priority

    def __repr__(self):
        return 'operobj({},{})'.format(self.base, self.priority, self.func)

    def __gt__(self, other):
        return self.priority > other.priority

    def eval(self, eles, locls):
        if __debug__:
            assert eles.base is self
            import control
            assert self.base in control.allopers, str(self) + " needs to be in control.allopers!"
            assert self.func == None, str(self) +" can't be in control.functions & have a fun\
(supposed to be defined in inbuiltfuncs)"
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

class numobj(obj):
    """
    The class that represents a number.
    This will probably be subclassed in the future.
    """
    TYPES = (int, float, complex)
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, numobj.TYPES), type(base)
        super().__init__(base)
    def __repr__(self):
        return 'numobj({})'.format(self.base)

    @staticmethod
    def fromstr(base):
        for typ in numobj.TYPES:
            try:
                return numobj(typ(base))
            except:
                pass
        raise SyntaxError("Cannot convert string '{}' to numobj".format(base))

class boolobj(numobj):
    """
    The class that represents a boolean.
    """
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, bool), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'boolobj({})'.format(self.base)

class arrayobj(numobj):
    """
    The class that represents an array.
    """
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, list), type(base) #atm, no tuples or sets or whatnot
        super().__init__(base)
    def __repr__(self):
        return 'arrayobj({})'.format(self.base)






