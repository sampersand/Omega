from Objects.Obj import obj
class numobj(obj):
    """
    The super class for all numbers.
    """
    def __init__(self, base = None):
        if base == None:
            base = 0
        if __debug__:
            assert isinstance(base, (int, float, complex)), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'numobj({})'.format(self.base)

    @staticmethod
    def frombase(base, control):
        return None if not base.isnumeric() else numobj(int(base))

    def eval(self, args, ldict):
        if __debug__:
            assert not args and args.base is self, 'just a thing i noticed'
        ldict.lastval = args
