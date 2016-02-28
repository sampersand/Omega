from Objects.Obj import obj
class strobj(obj):
    """
    The super class for all numbers.
    """
    def __init__(self, base = None):
        raise NotImplementedError('todo: this!')
        if base == None:
            base = 0
        super().__init__(base)

    def __repr__(self):
        return 'strobj({})'.format(self.base)

    @staticmethod
    def frombase(base, control):
        return None if len(base) < 2 or base[0] in control.allquotes and base[0] in control.allquotes else strobj(base)

    def eval(self, args, ldict):
        raise NotImplementedError()