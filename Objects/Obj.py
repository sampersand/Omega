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

    def _func_pow(self, obj1, obj2): return obj1.data ** obj2.data
    def _func_mul(self, obj1, obj2): return obj1.data * obj2.data
    def _func_div(self, obj1, obj2): return obj1.data / obj2.data
    def _func_mod(self, obj1, obj2): return obj1.data % obj2.data
    def _func_add(self, obj1, obj2): return obj1.data + obj2.data
    def _func_sub(self, obj1, obj2): return obj1.data - obj2.data
    def _func_rshift(self, obj1, obj2): return obj1.data >> obj2.data
    def _func_lshift(self, obj1, obj2): return obj1.data << obj2.data
    def _func_and(self, obj1, obj2): return obj1.data & obj2.data
    def _func_xor(self, obj1, obj2): return obj1.data ^ obj2.data
    def _func_or(self, obj1, obj2): return obj1.data | obj2.data
    def _func_lt(self, obj1, obj2): return obj1.data < obj2.data
    def _func_gt(self, obj1, obj2): return obj1.data > obj2.data
    def _func_le(self, obj1, obj2): return obj1.data <= obj2.data
    def _func_ge(self, obj1, obj2): return obj1.data >= obj2.data
    def _func_eq(self, obj1, obj2): return obj1.data == obj2.data
    def _func_ne(self, obj1, obj2): return obj1.data != obj2.data












