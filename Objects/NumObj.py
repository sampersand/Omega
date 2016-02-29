from Objects.Obj import obj
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
        #still very hacked together. TODO: regex for this.
        if '.' in base: 
            from Objects.FloatObj import floatobj
            return floatobj(float(base))
        if not base.isnumeric():
            return None
        from Objects.IntObj import intobj
        return intobj(int(base))
