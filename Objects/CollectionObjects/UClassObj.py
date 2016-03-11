from Objects import collectionobj, mthdobj, obj
from Group import group
class uclassobj(collectionobj):
    def _evalargs(self, args, lcls):
        ret = super()._evalargs(args, lcls)
        if ret != NotImplemented:
            return ret
        funcname = str(args[0])
        if __debug__:
            assert isinstance(lcls.iv.last.baseobj, uclassobj), 'Cannot apply class functions to a non-class object!'
        for line in lcls.iv.last:
            if isinstance(line.baseobj, mthdobj):
                
                lcls.iv.last = line
                r = group(data = lcls.iv.last[0].datastr, baseobj = obj(), control = args.control, args = args[1:])
                print(repr(r),"@aoihefoiahwef")
                quit(repr(lcls.iv.last))
                r.evalgrp(lcls)
                print(lcls)
                return 
                # quit(lcls)
                # return line.evalgrp(lcls)
        raise ValueError("Function '{}' isn't defined for {} '{}'".format(funcname, type(self).__qualname__, args))
