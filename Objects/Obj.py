class obj(object):
    _pyobj = None
    def __repr__(self):
        return type(self).__qualname__ + '()'

    def evalobj(self, args, lcls):
        if __debug__:
            from Group import group
            assert isinstance(args, group), args
        # if str(args) in lcls:
            # lcls[str(args)].baseobj.evalobj(args, lcls)
        if str(args.data) in args.control.delims['applier']:
            assert 0, 'todo! ' + str(args)
        else:
            lcls.iv.last = args.deepcopy()
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

    def _topyobj(self, pobj): return pobj if self._pyobj == None else self._pyobj(pobj)
    def _func_pow(self, obj1, obj2):    return self._topyobj(obj1.data) ** self._topyobj(obj2.data)
    def _func_mul(self, obj1, obj2):    return self._topyobj(obj1.data) * self._topyobj(obj2.data)
    def _func_div(self, obj1, obj2):    return self._topyobj(obj1.data) / self._topyobj(obj2.data)
    def _func_mod(self, obj1, obj2):    return self._topyobj(obj1.data) % self._topyobj(obj2.data)
    def _func_add(self, obj1, obj2):    return self._topyobj(obj1.data) + self._topyobj(obj2.data)
    def _func_sub(self, obj1, obj2):    return self._topyobj(obj1.data) - self._topyobj(obj2.data)
    def _func_rshift(self, obj1, obj2): return self._topyobj(obj1.data) >> self._topyobj(obj2.data)
    def _func_lshift(self, obj1, obj2): return self._topyobj(obj1.data) << self._topyobj(obj2.data)
    def _func_and(self, obj1, obj2):    return self._topyobj(obj1.data) & self._topyobj(obj2.data)
    def _func_xor(self, obj1, obj2):    return self._topyobj(obj1.data) ^ self._topyobj(obj2.data)
    def _func_or(self, obj1, obj2):     return self._topyobj(obj1.data) | self._topyobj(obj2.data)
    def _func_lt(self, obj1, obj2):     return self._topyobj(obj1.data) < self._topyobj(obj2.data)
    def _func_gt(self, obj1, obj2):     return self._topyobj(obj1.data) > self._topyobj(obj2.data)
    def _func_le(self, obj1, obj2):     return self._topyobj(obj1.data) <= self._topyobj(obj2.data)
    def _func_ge(self, obj1, obj2):     return self._topyobj(obj1.data) >= self._topyobj(obj2.data)
    def _func_eq(self, obj1, obj2):     return self._topyobj(obj1.data) == self._topyobj(obj2.data)
    def _func_ne(self, obj1, obj2):     return self._topyobj(obj1.data) != self._topyobj(obj2.data)

    def _ifunc_pow(self, obj1, obj2):  obj1.data = self._func_pow(obj1, obj2)
    def _ifunc_mul(self, obj1, obj2):  obj1.data = self._func_mul(obj1, obj2)
    def _ifunc_div(self, obj1, obj2):  obj1.data = self._func_div(obj1, obj2)
    def _ifunc_mod(self, obj1, obj2):  obj1.data = self._func_mod(obj1, obj2)
    def _ifunc_add(self, obj1, obj2):  obj1.data = self._func_add(obj1, obj2)
    def _ifunc_sub(self, obj1, obj2):  obj1.data = self._func_sub(obj1, obj2)
    def _ifunc_rshift(self, obj1, obj2):  obj1.data._f = selfunc_rshift(obj1, obj2)
    def _ifunc_lshift(self, obj1, obj2):  obj1.data._f = selfunc_lshift(obj1, obj2)
    def _ifunc_and(self, obj1, obj2):  obj1.data = self._func_and(obj1, obj2)
    def _ifunc_xor(self, obj1, obj2):  obj1.data = self._func_xor(obj1, obj2)
    def _ifunc_or(self, obj1, obj2):  obj1.dat = selfa._func_or(obj1, obj2)












