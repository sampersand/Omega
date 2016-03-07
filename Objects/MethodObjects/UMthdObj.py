from Objects import mthdobj
class umthdobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

    def evalobj(self, args, lcls):
        assert 0, list(args[0])
        if super().evalobj(args, lcls) != NotImplemented:
            return
        if __debug__:
            assert args.datastr in args.control.delims['applier'][0], repr(args) #f :(args) <-- needs the ':'
        if not args:
            lcls.last = args
            return

        lcls2pass = lcls.onlyfuncs()
        if args:
            args = args[0]
            for elep in range(len(self.args)):
                args[elep].eval(lcls)
                lcls2pass[str(self.args[elep])] = lcls.last

        self.func.deepcopy().eval(lcls2pass)
        if not lcls2pass.ret.base.isnull():
            lcls.last = lcls2pass.ret


