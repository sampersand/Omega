from Objects import obj, intobj
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

    def eval(self, args, ldict):
        if not args:
            ldict.last = self
            return
        try:
            super().eval(args, ldict)
        except SyntaxError:
            name = str(args[0])
            if name == 'len':
                if __debug__:
                    assert len(args) == 1, 'array:len'
                ldict.last = args.newgroup(intobj(len(self.base)))
            elif name == 'get':
                if __debug__:
                    assert len(args) == 2, 'array:get:pos'
                args[1].eval(ldict)
                ldict.last = self.base[ldict.last.base.base]
            elif name == 'add':
                if __debug__:
                    assert len(args) == 2, 'array:add:(pos, ele) or array:add:(ele,) not '+ str(args)
                if len(args[1]) == 2:
                    args[1][0].eval(ldict)
                    pos = ldict.last.base.base
                else:
                    pos = -1
                args[1][len(args[1]) == 2].eval(ldict)
                self.base.insert(pos, ldict.last)
                ldict.last = self.base[pos]
            else:
                raise SyntaxError("Unknown array function '{}' with parameters '{}'!".format(name,
                    len(args) >1 and args[1:] or ''))






