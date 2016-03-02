from Objects import obj
class typeobj(obj):
    """
    The class that represents a boolean.
    """
    def __init__(self, base = None):
        if base == None:
            base = type()
        if __debug__:
            assert isinstance(base, type), type(base)
        super().__init__(base)
        
    def __repr__(self):
        return 'typeobj({})'.format(self.base)