from Objects import obj
class numobj(obj):
    def evalobj(self, args, lcls, iflcls = True, docopy = True, throwfunc = True):
        if super().evalobj(args, lcls, throwfunc = False) == None:
            return
        return 0.5 #which one?
