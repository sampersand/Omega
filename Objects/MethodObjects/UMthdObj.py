from Objects import mthdobj
class umthdobj(mthdobj):
    def __init__(self, name, params, body):
        super().__init__(name)
        self.params = params
        self.body = body
    def __repr__(self):
        return super().__repr__().replace(')', ', %r, %r)' % (self.params, self.body))
    def evalobj(self, args, lcls):
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


