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
        if name == 'disp':
            self._disp(args, ldict)
        elif name == 'if':
            self._if(args, ldict)
        elif name == 'skip':
            self._skip(args, ldict)
        elif name == 'rm':
            self._rm(args, ldict)
        elif name == 'whilst':
            self._whilst(args, ldict)
        elif name == 'abort':
            self._abort(args, ldict)
        elif name == 'for':
            self._for(args, ldict)
        elif name == 'func':
            self._func(args, ldict)
        elif name == 'return':
            self._return(args, ldict)
        elif name == 'om':
            self._om(args, ldict)
        elif name == 'escape':
            self._escape(args, ldict)
        else:
            raise SyntaxError("Unknown Function '{}' with arguments '{}'! Known Functions: {}".format(self, args, 
                                                                                        args.control.funcs.keys()))
    def _disp(self, args, ldict):
        dispargs, sep, end = [''], ', ', '\n'
        if len(args) > 0:
            def scrub(pdispargs, ldict):
                for disparg in pdispargs:
                    disparg.eval(ldict)
                    yield ldict.lastval.base.scrubstr(args.control)
            dispargs = [x for x in scrub(args[0], ldict)]
            if len(args) > 1:
                if not args[1].base.isnull():
                    sep = args[1].base.scrubstr(args.control)
                if len(args) > 2:
                    if not args[2].base.isnull():
                        end = args[2].base.scrubstr(args.control)
        print(*dispargs, sep = sep, end = end)
    def _if(self, args, ldict):
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
    def _rm(self, args, ldict):
        if not args:
            ldict.clear()
        else:
            if __debug__:
                assert len(args) == 1, "only 1 thing after the semicolon... " + str(args)
                assert args, 'same reason as above'
            for ele in args[0]:
                ldict.lastval = ldict[str(ele)]
                del ldict[str(ele)]
    def _skip(self, args, ldict):
        pass #keep this here.
    def _whilst(self, args, ldict):
        if __debug__:
            assert len(args) == 2, 'whilst:(cond):(statement(s))'
        while True:
            args[0].eval(ldict) #evaluate the condition
            if not ldict.lastval.base:
                break
            args[1].eval(ldict) #execute the statement(s)
    def _abort(self, args, ldict):
        if len(args) == 1: #abort w/ message
            args[0].eval(ldict)
        else:
            del ldict.lastval # resets
        quit('Aborting!' + (" Message: " + str(ldict.lastval) if ldict.haslast() else ''))
    def _for(self, args, ldict):
        if __debug__:
            assert len(args) == 2, 'for:(init;cond;inc):(statement(s))'
            assert len(args[0]) == 3, 'for:(init;cond;inc):(statement(s))'
        args[0][0].eval(ldict) #initialization
        while True:
            args[0][1].eval(ldict) #evaluate the condition
            if not ldict.lastval.base:
                break
            args[1].eval(ldict) #execute the statement(s)
            args[0][2].eval(ldict) #increment
    def _func(self, args, ldict):
        from Group import group
        from Objects import userfuncobj
        args[0].eval(ldict)
        name = str(ldict.lastval)
        ldict[name] = group(base = userfuncobj(name, args[1], args[2]))
        ldict.lv = ldict[name]

    def _return(self, args, ldict):
        #Watch out! return:a+b is {return:a} + b
        args[0].eval(ldict)
        ldict.retval = ldict.lastval

    def _escape(self, args, ldict):
        #Watch out! return:a+b is {return:a} + b
        from Group import group
        ldict.escapeval = group
    def _om(self, args, ldict):
        if __debug__:
            assert len(args) > 0, "currently '{}' doesn't support empty function calls!".format(self)
        name = str(args[0])
        if name == 'rand':
            import random
            from Objects.FloatObj import floatobj
            from Group import group
            ldict.lastval = group(base = floatobj(random.random()))
        elif name == 'ldict' or name == 'locals':
            from Objects.DictObj import dictobj
            from Group import group
            ldict.lastval = group(base = dictobj(ldict.deepcopy()))
            del ldict.lastval.base.base.lastval
            # del ldict.lastval.base.base.lastval
        else:
            raise SyntaxError("No known '{}' function '{}' with arguments '{}'!".format(self, name, 
                                                                                        '' if len(args) == 0 else \
                                                                                        args[1:]))




















