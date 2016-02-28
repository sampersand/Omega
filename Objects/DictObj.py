from Objects.Obj import obj
class dictobj(obj):
    def __init__(self, base = None):
        if base == None:
            base = {}
        if __debug__:
            assert isinstance(base, dict), type(base)
        super().__init__(base)
    def __repr__(self):
        return 'dictobj({})'.format(self.base)