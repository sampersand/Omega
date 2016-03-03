from Objects import obj
class methodobj(obj):
    """
    The class that represents a function.
    """
    def __init__(self, base, func = None):
        if func == None:
            func = None #yes, it looks stupid, but it's here so it cant get overrided later
        super().__init__(base)
        self.func = func

    def __repr__(self):
        return 'methodobj({},base={})'.format(self.func, self.base)