from Objects import obj
class strobj(obj):
    """
    The super class for all numbers.
    """
    def __init__(self, base = None):
        if base == None:
            base = str()
        if __debug__:
            assert isinstance(base, str), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'strobj({})'.format(self.base)

    @staticmethod
    def frombase(base, control):
        return strobj(base) if len(base) > 1 and base[0] in control.allquotes and base[0] in control.allquotes else None

    def scrubstr(self, control):
        base = self.base
        for c in control.escapechars:
            base = base.replace(c, control.escapechars[c])
        if base and base[0] in control.allquotes:  base = base[1:]
        if base and base[-1] in control.allquotes: base = base[:-1]
        return base
