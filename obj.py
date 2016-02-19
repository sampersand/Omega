class obj():
    def __init__(self, base):
        if __debug__:
            assert not isinstance(base, obj), type(obj) #only allowed to pass non-objs
        self.base = base
    @staticmethod
    def frombase(ele):
        """ used when passing a string to determine which base to use """
        if __debug__:
            assert isinstance(ele, str) #can only read strs. otherwise, use appropriate subclass.
        return obj(ele)

    def __getattr__(self, attr):
        return self.base.__getattr__(attr)

    def __str__(self):
        return str(self.base)

    def __repr__(self):
        return 'obj({})'.format(self.base)

class funcobj(obj):
    def __init__(self, func, base = None):
        #warning this is backwards...
        super().__init__(base)
        if __debug__:
            assert func == None or hasattr(func, '__call__'), type(func)
        self.func = func
    def __repr__(self):
        return 'funcobj({},base={})'.format(self.func, self.base)

class operobj(funcobj):
    def __init__(self, base, priority, func = None):
        super().__init__(func, base)
        self.priority = priority
    def __repr__(self):
        return 'operobj({},{},func={})'.format(self.base, self.priority, self.func)

class nullobj(obj):
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return 'nullobj()'

class numobj(obj):
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, (int, float, complex)), type(base)
        super().__init__(base)

class boolobj(numobj):
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, bool), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'boolobj({})'.format(self.base)
n = numobj
no = n(1.0)
print(repr(no),str(no))