class obj():
    """
    The base class for all of the objects.
    """

    def __init__(self, base):
        if __debug__:
            assert not isinstance(base, obj), type(obj) #only allowed to pass non-objs
        self.base = base

    def __repr__(self):
        return 'obj({})'.format(self.base)

    def __str__(self):
        return str(self.base)

class funcobj(obj):
    """
    The class that represents a function.
    """
    def __init__(self, base, func = None):
        if func == None:
            func = None #yes, it looks stupid, but it's here so it cant get overrided later
        super().__init__(base)
        self.func = func

    def __repr__(self):
        return 'funcobj({},base={})'.format(self.func, self.base)

class operobj(funcobj):
    """
    The class that represents operators on objects.
    """
    def __init__(self, base, priority):
        super().__init__(base, None)
        self.priority = priority

    def __repr__(self):
        return 'operobj({},{})'.format(self.base, self.priority)

class nullobj(obj):
    """
    The class that represents a null object.
    In reality, it is representing a 'None' object type, but there is no way to access 'None'.
    """
    def __init__(self, isuser = False):
        super().__init__(None)
        self.isuser = isuser

    def __repr__(self):
        return 'nullobj()'

    def isnull(self):
        return not self.isuser

    def __str__(self):
        return 'null'

class numobj(obj):
    """
    The super class for all numbers.
    """
    def __init__(self, base = None):
        if base == None:
            base = 0
        super().__init__(base)

    def __repr__(self):
        return 'numobj({})'.format(self.base)

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























