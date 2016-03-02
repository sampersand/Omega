from Objects import obj
class strobj(obj):
    """
    The super class for all numbers.
    """
    def __init__(self, base = None, quotes = ('', '')):
        if base == None:
            base = str()
        if __debug__:
            assert isinstance(base, str), type(base)
        super().__init__(base)
        self.quotes = quotes

    def __repr__(self):
        return 'strobj({},quotes={})'.format(self.base, self.quotes)

    @staticmethod
    def fromstr(base, control):
        if base and base[0] in control.allquotes and base and base[-1] in control.allquotes: 
                return strobj(base = base[1:-1], quotes = (base[0], base[-1]))
        else:
            return None

    def scrubstr(self, control):
        base = self.base
        for c in control.escapechars:
            base = base.replace(c, control.escapechars[c])
        return base

    def _func_add    (self, other): return self.base + str(other.base) #this thing's base shbould be a str already