from Objects import numobj
class intobj(numobj):
    def evalobj(self, arg, lcls):
        super().evalobj(arg, lcls) #this is a lil sketchy, i need a better way to do this.
        lcls.iv.last = arg.deepcopy()
        print(repr(lcls),'@')

    def _func_pow(self, obj1, obj2):   return int(obj1.data) ** int(obj2.data)
    def _func_mul(self, obj1, obj2):   return int(obj1.data) * int(obj2.data)
    def _func_div(self, obj1, obj2):   return int(obj1.data) / int(obj2.data)
    def _func_mod(self, obj1, obj2):   return int(obj1.data) % int(obj2.data)
    def _func_add(self, obj1, obj2):   return int(obj1.data) + int(obj2.data)
    def _func_sub(self, obj1, obj2):   return int(obj1.data) - int(obj2.data)
    def _func_rshift(self, obj1, obj2):return int(obj1.data) >> int(obj2.data)
    def _func_lshift(self, obj1, obj2):return int(obj1.data) << int(obj2.data)
    def _func_and(self, obj1, obj2):   return int(obj1.data) & int(obj2.data)
    def _func_xor(self, obj1, obj2):   return int(obj1.data) ^ int(obj2.data)
    def _func_or(self, obj1, obj2):    return int(obj1.data) | int(obj2.data)
    def _func_lt(self, obj1, obj2):    return int(obj1.data) < int(obj2.data)
    def _func_gt(self, obj1, obj2):    return int(obj1.data) > int(obj2.data)
    def _func_le(self, obj1, obj2):    return int(obj1.data) <= int(obj2.data)
    def _func_ge(self, obj1, obj2):    return int(obj1.data) >= int(obj2.data)
    # def _func_eq(self, obj1, obj2):     return obj1.data == obj2.data #already defined
    # def _func_ne(self, obj1, obj2):     return obj1.data != obj2.data #already defined
