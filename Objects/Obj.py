import copy
class obj(object):
    _pyobj = None
    def __repr__(self):
        return type(self).__qualname__ + '()'

    def evalobj(self, args, lcls, iflcls = True, docopy = True, throwfunc = True):
        """ The functions every object has. 
            Currently, they are only `copy` and `type`.

            If `iflcls` is true, and `args.datastr in lcls`, then it will set `lcls.iv.last` to `lcls[args.datastr]`.
            If `docopy` is true, and there is no other viable way to evaluate it (i.e. `iflcls` is false / didn't work),
            it will just set `lcls.iv.last` to `args.deepcopy()`.
            if `throwfunc` is true, and args contains a function (`args.datastr in args.control.delims['applier']`),
            but the function isn't recognized, it will throw a syntax error.

            If throwfunc is false, and there is an unknown function, it will return 0.
            If docopy if false, and there is no other viable way toe valuate it, it will return 1
            """
        if __debug__:
            from Group import group
            assert isinstance(args, group), args
        if iflcls and args.datastr in lcls:
            lcls.iv.last = lcls[args.datastr]
            return
        if args.datastr in args.control.delims['applier']:
            if __debug__:
                assert len(args) > 0, "No known Obj function '{}' for Obj '{}'!".format(args, self)
            # objname = str(lcls.iv.last.data)
            fncname = str(args[0])
            if fncname in {'clone', 'copy'}:
                lcls.iv.last = lcls.iv.last.deepcopy()
            elif fncname == 'updtype':
                if __debug__:
                    from Objects import arrayobj
                    assert isinstance(args[1].baseobj, arrayobj), str(args) + " should be obj:updtype:(type)"
                    assert len(args[1]) == 1, str(args) + " should be obj:updtype:(type)"
                last = lcls.iv.last
                args[1][0].evalgrp(lcls)
                if __debug__:
                    from Objects import typeobj
                    assert isinstance(lcls.iv.last.baseobj, typeobj), "should be obj:updtype:(type)"
                last.baseobj = lcls.iv.last.baseobj.baseclass.baseobj
            elif fncname == 'type':
                from Group import group # not sure this is the best way
                from Objects import typeobj # to be doing this...
                lcls.iv.last = group(data = type(lcls.iv.last.baseobj).__qualname__,
                                     baseobj = typeobj(lcls.iv.last),
                                     control = args.control)
                # lcls.iv.copylast().data = lcls.iv.last.baseobj
            else:
                if not throwfunc:
                    return 0
                raise SyntaxError("No known '{}' function '{}'!".format(type(self).__qualname__, fncname))
            
        else:
            if not docopy:
                return 1
            lcls.iv.last = args.deepcopy()

    def _topyobj(self, objinstance): return objinstance if self._pyobj == None else self._pyobj(objinstance)
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












