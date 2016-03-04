from Objects import methodobj, obj
import Objects.OmFuncs
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
        if self.base[0] == ldict.IVAL_PREF:
            return ldict.last
        if self is args.base and not args: #aka, no params passed, then just do whatever is done normally.
            return super().eval(args, ldict)
        name = str(self)
        if __debug__:
            assert name in args.control.funcs,\
                "In-built Function '{}' isn't a known function: {}".format(self, args.control.funcs)
        if   name == 'if':      self._if(args, ldict)
        elif name == 'for':     self._for(args, ldict)
        elif name == 'return':  self._return(args, ldict)
        elif name == 'whilst':  self._whilst(args, ldict)
        elif name == 'disp':    self._disp(args, ldict)
        elif name == 'func':    self._func(args, ldict)
        elif name == 'abort':   self._abort(args, ldict)
        elif name == 'om':      self._om(args, ldict)
        elif name == 'input':   self._input(args, ldict)
        elif name == 'escape':  self._escape(args, ldict)
        elif name == 'rm':      self._rm(args, ldict)
        elif name == 'skip':    self._skip(args, ldict)
        else: raise SyntaxError("Unknown Function '{}' with arguments '{}'! Known Functions: {}".format(self, args,
                                                                                        args.control.funcs.keys()))
    def _disp(self, args, ldict):
        dispargs, sep, end = [''], ' ', '\n'
        if len(args) > 0:
            def scrub(pdispargs, ldict):
                for disparg in pdispargs:
                    disparg.eval(ldict)
                    yield ldict.last.base.scrubstr(args.control)
            dispargs = [x for x in scrub(args[0], ldict)]
            if len(args) > 1:
                if not args[1].base.isnull():
                    sep = args[1].base.scrubstr(args.control)
                if len(args) > 2:
                    if not args[2].base.isnull():
                        end = args[2].base.scrubstr(args.control)
        print(*dispargs, sep = sep, end = end)
    def _if(self, args, ldict):
        cond, iftrue, iffalse = args[0], args.newgroup(None), args.newgroup(None)
        if len(args) > 1:
            iftrue = args[1]
            if len(args) > 2:
                iffalse = args[2]
                if __debug__:
                    if len(args) > 3:
                        raise SyntaxError('Not allowed to have more than 3 arguments for if statement(s)!')
        cond.eval(ldict)
        (iftrue if ldict.last.base else iffalse).eval(ldict)
    def _rm(self, args, ldict):
        if not args:
            ldict.clear()
        else:
            if __debug__:
                assert len(args) == 1, "only 1 thing after the semicolon... " + str(args)
                assert args, 'same reason as above'
            for ele in args[0]:
                ele.eval(ldict)
                if type(ldict.last.base) == obj: #aka, if it isn't a special object.
                    del ldict[str(ldict.last)] 
                else:
                    print("rm isn't working 100%", repr(ldict.last))
                    del ldict.last
                    # del ldict.last.base

                # ldict.last = ldict[str(ele)]
                # del ldict[str(ele)]
    def _skip(self, args, ldict):
        pass #keep this here.
    def _whilst(self, args, ldict):
        if __debug__:
            assert len(args) == 2, 'whilst:(cond):(statement(s))'
        while True:
            args[0].eval(ldict) #evaluate the condition
            if not ldict.last.base or ldict.escape:
                break
            args[1].eval(ldict) #execute the statement(s)
    def _abort(self, args, ldict):
        if len(args) == 1: #abort w/ message
            args[0].eval(ldict)
        else:
            del ldict.last # resets
        quit('Aborting!' + (" Message: " + str(ldict.last) if not ldict.last.isnull() else ''))
    def _for(self, args, ldict):
        if __debug__:
            assert len(args) == 2, 'for:(init;cond;inc):(statement(s))'
            assert len(args[0]) == 3, 'for:(init;cond;inc):(statement(s))'
        args[0][0].eval(ldict) #initialization
        while True:
            args[0][1].eval(ldict) #evaluate the condition
            if not ldict.last.base or ldict.escape:
                break
            args[1].eval(ldict) #execute the statement(s)
            args[0][2].eval(ldict) #increment
    def _func(self, args, ldict):
        args[0].eval(ldict)
        name = str(ldict.last)
        from Objects import userfuncobj
        ldict[name] = args.newgroup(userfuncobj(name, args[1], args[2]))
        ldict.last = ldict[name]

    def _return(self, args, ldict):
        #Watch out! return:a+b is {return:a} + b
        args[0].eval(ldict)
        ldict.ret = ldict.last

    def _escape(self, args, ldict):
        ldict.escape = True

    def _om(self, args, ldict):
        return Objects.OmFuncs.eval(self, args, ldict)
    def _input(self, args, ldict):
        from Objects import strobj #this could be moved to the top
        msg, valid, err = ldict.last.newgroup('> '), None, ldict.last.newgroup(strobj("Invalid input!"))
        if len(args) > 0:
            args[0].eval(ldict)
            msg = ldict.last
            if len(args) > 1:
                args[1].eval(ldict)
                valid = ldict.last
                if len(args) > 2:
                    args[2].eval(ldict)
                    err = ldict.last
                    if __debug__:
                        if len(args) > 3:
                            raise SyntaxError('input:[question,[valid results (array) [, error messg]]]')
        ldict.last = ldict.last.newgroup(base = strobj())
        if valid != None:
            valid.base = valid.base.convstr()
        while True:
            ldict.last.base.base = str(input(msg.base.scrubstr(args.control)))
            if valid == None:
                break
            if valid != None:
                if __debug__:
                    from Objects import arrayobj
                    assert isinstance(valid.base, arrayobj), 'Only accepts array of valid results!, not ' + str(type(valid))
                if ldict.last.base not in valid.base:
                    print(err.base.scrubstr(args.control))
                else:
                    break;
















