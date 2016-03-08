from Objects import obj
class nullobj(obj):
    def __init__(self, isuser = False):
        self.isuser = isuser
    def evalobj(self, args, lcls, iflcls = True, docopy = True, throwfunc = True):
        pass