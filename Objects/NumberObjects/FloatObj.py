from Objects import numobj
class floatobj(numobj):
    _pyobj = float
    def evalobj(self, args, lcls, iflcls = True, docopy = True, throwfunc = True):
        if super().evalobj(args, lcls) == None:
            return
