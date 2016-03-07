from Objects import mthdobj
class umthdobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

    def evalobj(self, args, lcls):
        if super().evalobj(args, lcls) != NotImplemented:
            return

        lcls2pass = lcls.onlyfuncs()
        name, params, body = lcls.iv.last.deepcopy()
        if __debug__:
            assert isinstance(lcls.iv.last.baseobj, umthdobj),\
                "evalobj of a umthdobj uses the last value as the function to execute!"
            assert args, "cannot evaluate a function with a base type of '{}'!".format(type(args))
            assert len(args) == 1, "Args needs to be an array!".format(args)
            args = args[0]
            assert not (len(args) or len(params)) or len(args) == len(params), "Expected {} ({}), got {} ({})"\
                .format(params, len(params), args, len(args))

        for argp in range(len(params)): #setting the args
            args[argp].evalgrp(lcls)
            lcls2pass[str(params[argp])] = lcls.iv.last

        body.deepcopy().evalgrp(lcls2pass)
        del lcls.iv.last
        # print(list(str(v) + ':'+str(k)+'\n' for v, k in lcls2pass.items()))
        if lcls2pass.iv.ret:
            lcls.iv.last = lcls2pass.iv.ret


