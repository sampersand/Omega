from Objects import obj, intre, floatre, complre
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
    def fromstr(base, control):
        ret = None
        if intre.fullmatch(base) != None:
            from Objects import intobj #very bad placing
            ret = intobj.fromstr(base, control)
        elif floatre.fullmatch(base) != None:
            from Objects import floatobj #very bad placing
            ret = floatobj.fromstr(base, control)
        elif complre.fullmatch(base) != None:
            from Objects import complobj #very bad placing
            ret = complobj.fromstr(base, control)
        return ret
