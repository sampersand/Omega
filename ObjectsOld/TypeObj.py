from Objects import obj
class typeobj(obj):
    """
    The class that represents an omega object type.
    """
    def __init__(self, base = None, baseobj = None):
        if base == None:
            base = type()
        if __debug__:
            assert isinstance(base, type), type(base)
        super().__init__(base)
        self.baseobj = baseobj
        
    def __repr__(self):
        return 'typeobj({}{})'.format(self.base, ',baseobj=' + repr(baseobj) if baseobj != None else '')

    def updatebase(self, other, fname):
        # quit('"{}"\t\t"{}"\t\t"{}".'.format(self,other,fname))
        self.baseobj.updatebase(other, fname)
        quit(repr(self.baseobj))
        # if   fname == '': self.base = other.base