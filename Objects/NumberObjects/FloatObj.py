from Objects import numobj
class floatobj(numobj):
    _pyobj = float
    def evalobj(self, args, lcls):
        if super().evalobj(args, lcls) == None:
            return
