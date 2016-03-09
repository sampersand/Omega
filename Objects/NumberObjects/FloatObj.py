from Objects import numobj, intobj
class floatobj(numobj):
    _pyobj = float
    def _evalargs(self, args, lcls):
        ret = super()._evalargs(args, lcls)
        if ret != NotImplemented:
            return ret
        if __debug__:
            assert len(args) > 0, "No known '{}' function '{}'!".format(type(self).__qualname__, args)
        fncname = str(args[0])
        if fncname == 'round':
            lcls.iv.last.baseobj = intobj()
            lcls.iv.last.data = int(lcls.iv.last.data)
        else:
            raise SyntaxError("No known '{}' function '{}'!".format(type(self).__qualname__, fncname))

