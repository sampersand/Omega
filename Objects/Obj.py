class obj(object):
    def __repr__(self):
        return type(self).__qualname__ + '()'

    def evalobj(self, arg, lcls):
        if str(arg) in lcls:
            return locls[arg].bobj.eval(arg, lcls)
        elif str(arg.data) in arg.control.delims['applier']:
            assert 0, 'todo! ' + str(arg)
        else:
            lcls.last = arg.dcopy()
        # if str(args.base)
        # if str(self) in ldict:
        #     #this is ignoring the parens...
        #     ldict[str(self)].base.eval(args, ldict)
        # else:
        #     if str(args.base) in args.control.delims['applier']:
        #         if __debug__:
        #             assert len(args) > 0, "No known Obj function '{}' for Obj '{}'!".format(args, self)
        #         name = str(args[0])
        #         if name == 'copy':
        #             ldict.last = ldict.last.deepcopy()
        #         if name == 'type':
        #             ldict.last.base = ldict.last.base.objtype
        #         else:
        #             raise SyntaxError("No known Obj function '{}' for Obj '{}'!".format(args, self))
        #     else:
        #         if __debug__:
        #             assert args.base is self, "The argument's base ({}) isn't this base ({}) !".format(args.base, self.base)
        #         ldict.last = args.deepcopy()
