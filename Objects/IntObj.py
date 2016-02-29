from Objects.NumObj import numobj
class intobj(numobj):
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, int), type(base)
        super().__init__(base)
    def __repr__(self):
        return 'intobj({})'.format(self.base)
