import copy
class obj(object):
    _pyobj = None
    def __repr__(self):
        return type(self).__qualname__ + '()'

    def evalobj(self, args, lcls):
        """ the funcitons every object has. if an object doesn't have it's own defined evalobj,
            and there are no other valid methods, it will copy itself.
            If the object does have it's own defiend evalobj, and there are no other valid methods,
            it will return NotImplemented instead."""
        if __debug__:
            from Group import group
            assert isinstance(args, group), args
        if type(args.baseobj) == obj and args.datastr in lcls:
            lcls[args.datastr].evalgrp(lcls)
            lcls.iv.last = lcls[args.datastr]
            return
        # if args.datastr in lcls:
        #     if type(self).evalobj != obj.evalobj: #not sure this is correct, but it seems to be working
        #         return NotImplemented
        #     lcls[args.datastr].evalgrp(lcls)
        #     lcls.iv.last = lcls[args.datastr]
        #     return
        if args.datastr in args.control.delims['applier']:
            if __debug__:
                assert len(args) > 0, "No known Obj function '{}' for Obj '{}'!".format(args, self)
            # objname = str(lcls.iv.last.data)
            fncname = str(args[0])
            if fncname == 'copy':
                lcls.iv.last = lcls.iv.last.deepcopy()
            elif fncname == 'type':
                lcls.iv.copylast().data = lcls.iv.last.baseobj
            else:
                raise SyntaxError("No known Obj function '{}' for Obj '{}'!".format(args, self))
            
        else:
            if type(self).evalobj is obj.evalobj:
                lcls.iv.last = args.deepcopy()
            else:
                return NotImplemented

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












