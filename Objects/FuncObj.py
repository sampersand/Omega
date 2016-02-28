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
        return 'funcobj({},base={})'.format(self.func, self.base)
    def eval(self, args, ldict):
        if self is args.base: #aka, no params passed, then just do whatever is done normally.
            return super().eval(args, ldict)
        name = str(self)
        if __debug__:
            assert name in args.control.funcs,\
                "In-built Function '{}' isn't a known function: {}".format(self, args.control.funcs)
        if __debug__:
            assert args, 'cannot pass lone arguments atm! ('+str(args)+")"
        if name == 'disp':
            dispargs, sep, end = [''], ', ', '\n'
            if len(args) > 0:
                def scrub(args, ldict):
                    print(repr(args),repr(ldict))
                    args.eval(ldict)
                    return ldict.lastval.base.scrubstr(args.control)
                dispargs = (scrub(args, ldict) for args in args[0])
                if len(args) > 1:
                    if not args[1].base.isnull():
                        sep = args[1].base.scrubstr(args.control)
                    if len(args) > 2:
                        if not args[2].base.isnull():
                            end = args[2].base.scrubstr(args.control)
                    
            # if name == 'disp':
            #     from obj import strobj
            #     args, sep, end = ('', ), ', ', '\n'
            #     if len(eles) > 0:
            #         if __debug__:
            #             assert not eles[0].base.isnull(), 'when would it be?'
            #         if not eles[0].base.isnull():
            #             if not eles[0]:
            #                 eles[0].eval(ldict)
            #                 args = (ldict.lv.base.strobj.scrub(), )
            #             else:
            #                 def scrub(ele, ldict):
            #                     print(repr(ele),repr(ldict))
            #                     ele.eval(ldict)
            #                     return ldict.lv.base.strobj.scrub()
            #                 args = [scrub(ele, ldict) for ele in eles[0]]
            #         if len(eles) > 1:
            #             if not eles[1].base.isnull():
            #                 if __debug__:
            #                     assert isinstance(eles[1].base, strobj)
            #                 sep = eles[1].base.scrub()
            #             if len(eles) > 2:
            #                 if not eles[2].base.isnull():
            #                     if __debug__:
            #                         assert isinstance(eles[2].base, strobj)
            #                     end = eles[2].base.scrub()
            print(*dispargs, sep = sep, end = end)
        else:
            raise SyntaxError("Unknown Function '{}' in arguments '{}'! Known Functions: {}".format(self, args, 
                                                                                        args.control.funcs.keys()))