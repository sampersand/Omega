from Objects.NumObj import numobj
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
    def eval(self, args, ldict):
        raise NotImplementedError()
