from Objects.NumObj import numobj
class floatobj(numobj):
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, float), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'floatobj({})'.format(self.base)

    def eval(self, args, ldict):
        try:
            super().eval(args, ldict)
        except SyntaxError:
            name = str(args[0])
            if name == 'round':
                from Objects.IntObj import intobj
                from Group import group
                ldict.lastval = group(base = intobj(round(self.base)))
