from Objects import numobj
class intobj(numobj):
    def evalobj(self, arg, lcls):
        super().evalobj(arg, lcls) #this is a lil sketchy, i need a better way to do this.
        lcls.iv.last.updatedata(int(arg.data), arg.baseobj)