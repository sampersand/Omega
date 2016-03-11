from Objects import mthdobj, boolobj, obj, arrayobj, umthdobj, uclassobj
from Group import group
from Locals import lcls as localsdict
class funcobj(mthdobj):
    def __init__(self, name = ''):
        super().__init__(name)

    def _evalargs(self, args, lcls):
        ret = super()._evalargs(args, lcls)
        if ret != NotImplemented:
            return ret
        name = "_" + self.name
        if name not in dir(self):
            if type(self) == funcobj:
                raise ValueError("Function '{}' isn't defined yet!".format(self.name))
            return NotImplemented
        self.__getattribute__(name)(args, lcls)

    def _disp(self, args, lcls):
        dispargs, sep, end = [''], ' ', '\n'
        if len(args) > 0:
            def scrub(pdispargs, lcls):
                for disparg in pdispargs:
                    disparg.evalgrp(lcls)
                    yield lcls.iv.last.scrubstr(args.control)
                    # yield lcls.iv.last.data.scrubstr(args.control)
            # dispargs = [x for x in scrub(args[0], lcls)]
            dispargs = scrub(args[0], lcls)
            if len(args) > 1:
                if args[1]:
                    args[1].evalgrp(lcls)
                    sep = lcls.iv.last.scrubstr(args.control)
                if len(args) > 2:
                    if args[2]:
                        args[2].evalgrp(lcls)
                        end = lcls.iv.last.scrubstr(args.control)
        print(*dispargs, sep = sep, end = end)
    def _if(self, args, lcls):
        cond, iftrue, iffalse = args[0], None, None
        if len(args) > 1:
            iftrue = args[1]
            if len(args) > 2:
                iffalse = args[2]
                if __debug__:
                    if len(args) > 3:
                        raise SyntaxError('Not allowed to have more than 3 arguments for if statement(s)!')
        cond.evalgrp(lcls)
        if iftrue != None and lcls.iv.last.data:
            iftrue.evalgrp(lcls)
        elif iffalse != None and not lcls.iv.last.data:
            iffalse.evalgrp(lcls)
    def _skip(self, args, lcls):
        """ literally nothing happens """
        pass #keep this here.
    def _abort(self, args, lcls):
        if len(args) == 1: #abort w/ message
            args[0].evalgrp(lcls)
        else:
            del lcls.iv.last # resets
        quit('Aborting!' + (" Message: " + str(lcls.iv.last) if lcls.iv.last else ''))
    def _whilst(self, args, lcls):
        if __debug__:
            assert len(args) == 2, 'whilst:(cond):(statement(s))'
        while True:
            args[0].evalgrp(lcls) #evaluate the condition
            if not lcls.iv.last.data or lcls.iv.esc:
                break
            args[1].evalgrp(lcls) #execute the statement(s)
    def _for(self, args, lcls):
        if __debug__:
            assert len(args) == 2, 'for:(init,cond,inc):(statement(s))'
            assert len(args[0]) == 3, 'for:(init,cond,inc):(statement(s))'
        args[0][0].evalgrp(lcls) #initialization
        while True:
            args[0][1].evalgrp(lcls) #evaluate the condition
            if not lcls.iv.last.data or lcls.iv.esc:
                break
            args[1].evalgrp(lcls) #execute the statement(s)
            args[0][2].evalgrp(lcls) #increment
    def _escape(self, args, lcls):
        lcls.iv.esc.data = True
        lcls.iv.esc.baseobj = boolobj()
    def _rm(self, args, lcls):
        if not len(args):
            lcls.clear()
        else:
            if __debug__:
                assert len(args) == 1, "only 1 thing after the semicolon... " + str(args)
                assert args, 'same reason as above'
            for arg in args[0]:
                if type(arg.baseobj) == obj: #aka, if it isn't a special object.
                    del lcls[str(arg)] 
                else:
                    del lcls.iv.last
    def _input(self, args, lcls):
        """ nput:[question,[valid results (regex) [, error messg]]]"""
        from Objects import strobj #this could be moved to the top
        msg, valid, err = group(data = "'> '", control = args.control), None,\
                          group(data = "\"\0'{inv}' is an invalid input! Valid: '{val}'.\"", control = args.control)
        if len(args) > 0:
            args[0].evalgrp(lcls)
            msg = lcls.iv.last
            if len(args) > 1:
                args[1].evalgrp(lcls)
                valid = lcls.iv.last
                if len(args) > 2:
                    args[2].evalgrp(lcls)
                    err = lcls.iv.last
                    if __debug__:
                        assert len(args) <= 3, 'input:[question,[valid results (array) [, error messg]]]'
        lcls.iv.last = group(baseobj = strobj(), control = args.control)
        # if valid != None:
        #     assert 0, 'what is convstr??' + repr(valid)
        #     valid.data = str(valid.data.convstr())
        while True:
            lcls.iv.last = group(data = str(input(msg.scrubstr(args.control))), control = args.control)
            if valid == None:
                break
            if __debug__:
                assert isinstance(valid.baseobj, arrayobj),\
                    'Only accepts array of valid results!, not ' + str(type(valid.baseobj))
            if lcls.iv.last not in valid:
                print(err.scrubstr(args.control, inv = lcls.iv.last.data, val = str(valid)))
            else:
                break;
    def _return(self, args, lcls):
        #Watch out! return:a+b is {return:a} + b
        args[0].evalgrp(lcls)
        lcls.iv.ret = lcls.iv.last

    def _func(self, args, lcls):
        if __debug__:
            assert len(args) == 3, 'func:name:params:body'
        lcls[str(args[0])] = group(data = args.datastr,
                               baseobj = umthdobj(str(args[0])),
                               args = list(args),
                               control = args.control)

    def _class(self, args, lcls):
        if __debug__:
            assert len(args) == 3, 'class:name:[(parent)]:(body)'


        lcls2pass = localsdict(args.control)
        args2pass = []
        if __debug__:
            assert len(args[2]) == 1, 'body should be :{body}, not' + str(args[2])
        for arg in args[2][0]:
            arg.evalgrp(lcls2pass)
            args2pass.append(lcls2pass.iv.last.deepcopy())
        lcls[str(args[0])] = group(data = args.datastr, 
                                baseobj = uclassobj(),
                                args = args2pass, 
                                control = args.control)
    



















