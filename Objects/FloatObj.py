from Objects.NumObj import numobj
class floatobj(numobj):
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, float), type(base)
        super().__init__(base)
    def __str__(self):
        return 'floatobj({})'.format(self.base)