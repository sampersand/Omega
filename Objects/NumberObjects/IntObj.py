from Objects import numobj
class intobj(numobj):
    def evalobj(self, arg, lcls):
        lcls.iv.last.updatedata(int(arg.data), arg.baseobj)