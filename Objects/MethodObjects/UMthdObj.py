from Objects import mthdobj
class umthdobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

    def evalobj(self, args, lcls):
        if super().evalobj(args, lcls) != NotImplemented:
            return

        lcls2pass = lcls.onlyfuncs()
        if __debug__:
            assert args, "cannot evaluate a function with a base type of '{}'!".format(type(args))
            assert len(args) == 2, "Args needs to be in the format [params, args], not '{}'!".format(args)
        params, funcbody = args
        assert 0, lcls
        for argp in range(len(args)): #setting the args
            args[argp].evalgrp(lcls)
            lcls2pass[str(args[argp])] = lcls.iv.last

        args[0] .deepcopy().eval(lcls2pass)
        if not lcls2pass.ret.base.isnull():
            lcls.last = lcls2pass.ret


