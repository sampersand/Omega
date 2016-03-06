from Objects import mthdobj
class funcobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

    def evalobj(self, args, lcls):
        if args.data == self.name:
            lcls.iv.last = args
            return
        if __debug__:
            assert '_' + self.name in dir(funcobj)
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