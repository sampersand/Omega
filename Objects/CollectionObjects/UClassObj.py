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
                    topass.iv.last = line
                    topass.iv.this = group(control = args.control, baseobj = uclassobj(),
                                           attrs = {'this' : lcls.iv.last})
                    delim = args.control.delims['applier']
                    topass.iv.last.baseobj.evalobj(group(data = delim[0], baseobj = delim[1], 
                                                       control = args.control, args = args), topass)
                    lcls.iv.last = topass.iv.this
                    return lcls.iv.last

        funcname = str(args[0])
        if __debug__:
            assert isinstance(lcls.iv.last.baseobj, uclassobj), 'Cannot apply class functions to a non-class object!'
        if __debug__:
            assert isinstance(lcls.iv.last.attrs['this'].baseobj, uclassobj), lcls.iv.last.attrs['this'].baseobj
        for line in lcls.iv.last.attrs['this']:
            if isinstance(line.baseobj, mthdobj) and line[0].datastr == funcname:
                topass = lclsdict(args.control)
                topass.iv.last = line
                topass.iv.this = group(control = args.control, baseobj = uclassobj(),
                                       attrs = {'this' : lcls.iv.last})
                delim = args.control.delims['applier']
                topass.iv.last.baseobj.evalobj(group(data = delim[0], baseobj = delim[1], 
                                                   control = args.control, args = args[1:]), topass)
                lcls.iv.last = topass.iv.last
                return lcls.iv.last
        raise ValueError("Function '{}' isn't defined for {} '{}'".format(funcname, type(self).__qualname__, args))















