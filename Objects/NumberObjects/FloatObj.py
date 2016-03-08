from Objects import numobj, intobj
class floatobj(numobj):
    _pyobj = float
    def evalobj(self, args, lcls, iflcls = True, docopy = True, throwfunc = True):
        if super().evalobj(args, lcls) == None:
            return
        if args.datastr in args.control.delims['applier']:
            if __debug__:
                assert len(args) > 0, "No known Obj function '{}' for Obj '{}'!".format(args, self)
            # objname = str(lcls.iv.last.data)
            fncname = str(args[0])
            if fncname == 'round':
                lcls.iv.last.baseobj = intobj()
            else:
                if not throwfunc:
                    return 0
                raise SyntaxError("No known '{}' function '{}'!".format(type(self).__qualname__, fncname))

