from Objects import obj
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
        from Objects import floatobj, intobj #very bad placing
        #still very hacked together. TODO: regex for this.
        if '.' in base: 
            return floatobj(float(base))
        if not base.isnumeric():
            return None
        return intobj(int(base))
