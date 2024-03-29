from Objects import mthdobj, arrayobj, userobj
class umthdobj(mthdobj, userobj):
    def __init__(self, name = ''):
        super().__init__(name)
    
    def _evalargs(self, args, lcls, ignore, origlcls=None):
        if not origlcls:
            origlcls = lcls
        ret = super()._evalargs(args, lcls, ignore)
        if ret != NotImplemented:
            return ret
        # if not isinstance(args, lcls)
        name, params, body = list(lcls.iv.last.deepcopy())
        lcls2pass = lcls.onlyuobjs()
        if __debug__:
            assert isinstance(lcls.iv.last.baseobj, umthdobj),\
                "evalobj of a umthdobj uses the last value as the function to execute!"
            assert args, "cannot evaluate a function with a base type of '{}'!".format(type(args))
            assert len(args) == 1, "Args needs to be an array!, not '{}' [ {}] ".format(args, args.baseobj)
        args = args[0]
        if __debug__:
            assert len(args) == len(params), "'{}' Expected '{}' ({}), got '{}' ({})"\
                .format(name, params, len(params), args, len(args))

        for argp in range(len(params)): #setting the args
            # print(lcls2pass, lcls,sep='\t\t|\t\t')
            args[argp].evalgrp(origlcls)
            lcls2pass[str(params[argp])] = origlcls.iv.last
        body.deepcopy().evalgrp(lcls2pass)
        del lcls.iv.last
        if lcls2pass.iv.ret:
            lcls.iv.last = lcls2pass.iv.ret

    def groupstr(self, grp) -> str:
        return super().groupstr(grp) if len(grp) != 3 else str(grp[0:2])