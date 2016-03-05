class obj(object):
    def __repr__(self):
        return type(self).__qualname__ + '()'

    def evalobj(self, args, lcls):
        if str(args) in lcls:
            return locls[args].baseobj.eval(args, lcls)
        elif str(args.data) in args.control.delims['applier']:
            assert 0, 'todo! ' + str(args)
        else:
            lcls.last = args.deepcopy()
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

    def _func_pow(self, other): return self.data ** other.data
    def _func_mul(self, other): return self.data * other.data
    def _func_div(self, other): return self.data / other.data
    def _func_mod(self, other): return self.data % other.data
    def _func_add(self, other): return self.data + other.data
    def _func_sub(self, other): return self.data - other.data
    def _func_rshift(self, other): return self.data >> other.data
    def _func_lshift(self, other): return self.data << other.data
    def _func_and(self, other): return self.data & other.data
    def _func_xor(self, other): return self.data ^ other.data
    def _func_or(self, other): return self.data | other.data
    def _func_lt(self, other): return self.data < other.data
    def _func_gt(self, other): return self.data > other.data
    def _func_le(self, other): return self.data <= other.data
    def _func_ge(self, other): return self.data >= other.data
    def _func_eq(self, other): return self.data == other.data
    def _func_ne(self, other): return self.data != other.data












