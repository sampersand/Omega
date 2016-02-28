from Objects.Obj import obj
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
            ldict.lastval = self
            return
        name = str(args[0])
        if name == 'get':
            if __debug__:
                assert len(args) == 2, 'array:get:pos'
            args[1].eval(ldict)
            ldict.lastval = self.base[ldict.lastval.base.base]
    #     if eles.base is self:
    #         locls.lv = eles
    #         return
    #     import inbuiltfuncs
    #     inbuiltfuncs.evalarray(self, eles, locls)







