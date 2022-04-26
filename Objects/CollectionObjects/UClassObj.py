from Objects import collectionobj, mthdobj, dictobj, userobj, arrayobj
from Group import group
from Locals import lcls as lclsdict
class uclassobj(collectionobj, userobj):

    @staticmethod
    def _classiter(cl):
        for line in cl:
            if isinstance(line.baseobj, mthdobj):
                yield line

    def _evalargs(self, args, lcls, ignore):
        funcname = str(args[0])
        if __debug__:
            assert isinstance(lcls.iv.last.baseobj, uclassobj), 'Cannot apply class functions to a non-class object!'
        if not lcls.iv.last.attrsnodata or list(lcls.iv.last.attrsnodata.keys()) == ['$__name']:
            whichone = lcls.iv.last 
        else:
            whichone = uclassobj._classiter(lcls.iv.last)
        for line in whichone:
            if isinstance(line.baseobj, mthdobj) and line[0].datastr == funcname:
                topass = lcls.onlyuobjs()
                # topass = lclsdict(args.control)
                topass.iv.last = line
                topass.iv.this = lcls.iv.last
                delim = args.control.delims['applier']
                # print(topass,group(data = delim[0], baseobj = delim[1], 
                                                   # control = args.control, args = args[1:]))
                topass.iv.last.baseobj._evalargs(group(data = delim[0], baseobj = delim[1],
                                                   control = args.control, args = args[1:]), topass, {}, lcls)
                lcls.iv.last = topass.iv.last.deepcopy()
                return lcls.iv.last
        if funcname == 'funcs':
            lcls.iv.last = group(data = ':', baseobj = arrayobj(),
                control = args.control, args = uclassobj._classiter(lcls.iv.last))
            return lcls.iv.last
        ret = super()._evalargs(args, lcls, ignore)
        if ret != NotImplemented:
            return ret
        raise ValueError("Function '{}' isn't defined for {} '{}'".format(funcname, type(self).__qualname__, args))

    def groupstr(self, grp):
        return super().groupstr(grp) if len(grp) != 3 else '<class ' + str(grp.attrs[grp._attrsdict['name']]) + '>'













