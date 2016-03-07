from Objects import mthdobj
class funcobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

    def evalobj(self, args, lcls):
        if args.data == self.name:
            lcls.iv.last = args
            return
        if __debug__:
            assert '_' + self.name in dir(funcobj), "Inbuilt Function '{}' isn't defined yet!".format(self.name)
        self.__getattribute__('_' + self.name)(args, lcls)

    def _disp(self, args, lcls):
        dispargs, sep, end = [''], ' ', '\n'
        if len(args) > 0:
            def scrub(pdispargs, lcls):
                for disparg in pdispargs:
                    disparg.evalgrp(lcls)
                    yield lcls.iv.last.scrubstr(args.control)
                    # yield lcls.iv.last.data.scrubstr(args.control)
            dispargs = [x for x in scrub(args[0], lcls)]
            if len(args) > 1:
                if args[1]:
                    sep = args[1].scrubstr(args.control)
                if len(args) > 2:
                    if args[2]:
                        end = args[2].scrubstr(args.control)
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
        assert 0, args
        args[0][0].eval(lcls) #initialization
        while True:
            args[0][1].eval(lcls) #evaluate the condition
            if not lcls.last.base or lcls.escape:
                break
            args[1].eval(lcls) #execute the statement(s)
            args[0][2].eval(lcls) #increment
    



















