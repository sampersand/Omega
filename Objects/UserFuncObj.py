from Objects import funcobj
class userfuncobj(funcobj):
    def __init__(self, base, args, func):
        super().__init__(base, func)
        self.args = args

    def __repr__(self):
        return 'userfuncobj({},{},{})'.format(self.base, self.args, self.func)

    def __str__(self):
        return super().__str__() + ':' + str(self.args)

    # def _genargs(self, args, ldict):
    def eval(self, args, ldict):
        if __debug__:
            assert args.basestr in args.control.delims['applier'][0] #f :(args) <-- needs the ':'
        if args.base is self:
            ldict.last = args
            return

        nldict = ldict.onlyfuncs()
        if args:
            args = args[0]
            for elep in range(len(self.args)):
                args[elep].eval(ldict)
                nldict[str(self.args[elep])] = ldict.last

        self.func.deepcopy().eval(nldict)
        if not nldict.ret.base.isnull():
            ldict.last = nldict.ret

