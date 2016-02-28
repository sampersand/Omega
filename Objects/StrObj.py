from Objects.Obj import obj
class strobj(obj):
    """
    The super class for all numbers.
    """
    def __init__(self, base = None):
        raise NotImplementedError('todo: this!' + str(base))
        if base == None:
            base = 0
        super().__init__(base)

    def __repr__(self):
        return 'strobj({})'.format(self.base)

    @staticmethod
    def frombase(base, control):
        return strobj(base) if len(base) > 1 and base[0] in control.allquotes and base[0] in control.allquotes else None

    def eval(self, args, ldict):
        raise NotImplementedError()