from Objects import obj
class typeobj(obj):
    def __init__(self, baseclass = None):
        self.baseclass = baseclass
    def __repr__(self):
        return super().__repr__().replace(')', '%r)' % self.baseclass)

    def evalobj(self, args, lcls):
        pass