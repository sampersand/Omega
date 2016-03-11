from Objects import collectionobj, mthdobj, obj, dictobj
from Group import group
from Locals import lcls as lclsdict
class uclassobj(collectionobj):

    @staticmethod
    def _classiter(cl):
        for line in cl:
            if isinstance(line.baseobj, mthdobj):
                yield line

    def _evalargs(self, args, lcls):

        ret = super()._evalargs(args, lcls)

        if ret != NotImplemented:
            return ret

        if len(args) == 1:
            for line in uclassobj._classiter(lcls.iv.last):
                if line[0].datastr == '$init':
                    
                    topass = lclsdict(args.control)
                    topass.iv.this = group(data = 'WHAT TO DO?', control = args.control, baseobj = uclassobj(),
                                           args = [group(data = '$lcls list', baseobj = dictobj(),
                                                        control = args.control,
                                                        attrs = {'a key' : 'a value'})])
                    topass.iv.last = line
                    delim = args.control.delims['applier']
                    topass.iv.last.baseobj.evalobj(group(data = delim[0], baseobj = delim[1], 
                                                       control = args.control, args = args), topass)
                    lcls.iv.last = topass.iv.this
            return 

        funcname = str(args[0])
        if __debug__:
            assert isinstance(lcls.iv.last.baseobj, uclassobj), 'Cannot apply class functions to a non-class object!'
        for line in lcls.iv.last:
            if isinstance(line.baseobj, mthdobj):

                lcls.iv.last = line
                delim = args.control.delims['applier']
                r = group(data = delim[0], baseobj = delim[1], control = args.control, args = args[1:])
                quit('todo!')
                quit(repr(lcls.iv.last))
                r.evalgrp(lcls)
                # print(repr(r),"@aoihefoiahwef")
                # print(lcls)
                return 
                # quit(lcls)
                # return line.evalgrp(lcls)
        raise ValueError("Function '{}' isn't defined for {} '{}'".format(funcname, type(self).__qualname__, args))
