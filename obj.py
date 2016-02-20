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
        locls['$'] = self.base

class funcobj(obj):
    """
    The class that represents a function.
    """
    def __init__(self, base, func = None):
        #warning this is backwards...
        super().__init__(base)
        if __debug__:
            assert func == None or hasattr(func, '__call__'), type(func)
        self.func = func

    def __repr__(self):
        return 'funcobj({},base={})'.format(self.func, self.base)

    def eval(self, eles, locls):
        if self.func == None:
            import builtins
            builtins

class operobj(funcobj):
    """
    The class that represents operators on objects.
    """
    def __init__(self, base, priority, func = None):
        super().__init__(base, func)
        self.priority = priority
    def __repr__(self):
        return 'operobj({},{},func={})'.format(self.base, self.priority, self.func)

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

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
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, (int, float, complex)), type(base)
        super().__init__(base)

class boolobj(numobj):
    """
    The classthat represents a boolean.
    """
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, bool), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'boolobj({})'.format(self.base)