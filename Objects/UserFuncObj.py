from Objects.FuncObj import funcobj
class userfuncobj(funcobj):
    def __init__(self, base, args, func):
        super().__init__(base, func)
        self.args = args

    def __repr__(self):
        return 'userfuncobj({},{},{})'.format(self.base, self.args, self.func)
    def __str__(self):
        return super().__str__() + ':' + str(self.args)
    def _genargs(self, args, ldict):
        ret = ldict.onlyfuncs()
        # if __debug__:
        #     assert len(args) == len(self.args), "{} args are required for '{}', got {} {}!".\
        #             format(len(self.args), self.base, len(args), str(args)[1:])
        for elep in range(len(self.args)):
            args[elep].eval(ldict)
            ret[str(self.args[elep])] = ldict.lastval
        return ret
    def eval(self, args, ldict):
        if __debug__:
            assert args.basestr in args.control.delims['applier'][0] #f :(args) <-- needs the ':'
        if args.base is self:
            ldict.lastval = args
            return
        from Group import group
        nldict = ldict.onlyfuncs() if not args else self._genargs(args[0], ldict)
        import copy
        copy.deepcopy(self.func).eval(nldict)
        if not nldict.retval.base.isnull():
            ldict.lastval = nldict.retval

