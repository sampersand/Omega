from Objects.MethodObj import methodobj
class funcobj(methodobj):
    """
    The class that represents an inbuilt function.
    """
    def __init__(self, base, func = None):
        if func == None:
            func = None #yes, it looks stupid, but it's here so it cant get overrided later
        super().__init__(base)
        self.func = func

    def __repr__(self):
        return 'funcobj({},func={})'.format(self.base, self.func)
    def eval(self, args, ldict):
        if self is args.base and not args: #aka, no params passed, then just do whatever is done normally.
            return super().eval(args, ldict)
        name = str(self)
        if __debug__:
            assert name in args.control.funcs,\
                "In-built Function '{}' isn't a known function: {}".format(self, args.control.funcs)
        # if __debug__:
            # assert args, 'cannot pass lone arguments atm! ('+str(args)+")"
        if name == 'disp':
            dispargs, sep, end = [''], ', ', '\n'
            if len(args) > 0:
                def scrub(pdispargs, ldict):
                    for disparg in pdispargs:
                        disparg.eval(ldict)
                        yield ldict.lastval.base.scrubstr(args.control)
                dispargs = scrub(args[0], ldict)
                if len(args) > 1:
                    if not args[1].base.isnull():
                        sep = args[1].base.scrubstr(args.control)
                    if len(args) > 2:
                        if not args[2].base.isnull():
                            end = args[2].base.scrubstr(args.control)
            print(*dispargs, sep = sep, end = end)
        elif name == 'if':
            from Group import group
            cond, iftrue, iffalse = args[0], group(), group()
            if len(args) > 1:
                iftrue = args[1]
                if len(args) > 2:
                    iffalse = args[2]
                    if __debug__:
                        if len(args) > 3:
                            raise SyntaxError('Not allowed to have more than 3 arguments for if statement(s)!')
            cond.eval(ldict)
            (iftrue if ldict.lastval.base else iffalse).eval(ldict)

        elif name == 'skip':
            pass #keep this here.
        elif name == 'rm':
            if not args:
                ldict.clear()
            else:
                if __debug__:
                    assert len(args) == 1, "only 1 thing after the semicolon... " + str(args)
                    assert args, 'same reason as above'
                for ele in args[0]:
                    ldict.lastval = ldict[str(ele)]
                    del ldict[str(ele)]
        else:
            raise SyntaxError("Unknown Function '{}' in arguments '{}'! Known Functions: {}".format(self, args, 
                                                                                        args.control.funcs.keys()))





















