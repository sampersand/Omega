import copy
from enum import Enum
class ObjTypes():
    class _objtyp():
        def __init__(self, defaultbase):
            self.dfb = defaultbase
        def __call__(self, base = ..., *args, **kwargs):
            if not args:
                return obj(self.dfb if base == ... else base, kwargs) #val will be true b/c it has a default base
            return obj([self.dfb if base == ... else base] + list(args), kwargs) #val will be true b/c it has a default base

        def __getattr__(self, attr):
            return self().__getattribute__(attr)
    obj    = _objtyp(None)
    strobj = _objtyp(str())
    intobj = _objtyp(int())
    floatobj = _objtyp(float())
    nullobj = _objtyp(None)
    methodobj = _objtyp(None)
    typeobj = _objtyp(None)
    numobj = _objtyp(None)
    boolobj = _objtyp(bool())
    dictobj = _objtyp(dict())
    arrayobj = _objtyp(list())
    funcobj = _objtyp(None)
    operobj = _objtyp(None)
    userfuncobj = _objtyp(None)
    lcls = dict(locals())
    _alldict = dict()
    for e in lcls:
        if e[-3:] == 'obj':
            _alldict[e] = lcls[e]

class obj():
    """
    The base class for all of the objects.
    """

    def __init__(self, base, otype = ObjTypes.obj):
        if __debug__:
            assert not isinstance(base, obj), type(base) #only allowed to pass non-objs
            # assert not isinstance(otype, ObjTypes), type(base) #only allowed to pass non-objs
        self.base = base
        self.otype = otype
    def __repr__(self):
        return 'obj({})'.format(self.base)

    def __str__(self):
        return str(self.base)

    def scrubstr(self, control):
        return str(self)

    @staticmethod
    def frombase(base, control):
        """
        Used when passing a string to determine which base to use.
        """
        
        if isinstance(base, obj):
            return base
        if base == None:
            from Objects import nullobj
            return nullobj()
        if __debug__:
            assert isinstance(base, str), type(base) #can only read strs. otherwise, use appropriate subclass.
        return obj.fromstr(base, control)

    @staticmethod
    def fromstr(base, control):
        if base in control.allkws:
            return control.allkws[base]
        from Objects import numobj, strobj #todo: put at the top of the file
        ret = numobj.fromstr(base, control)
        if ret == None:
            ret = strobj.fromstr(base, control)
            if ret == None:
                ret = obj(base)
        if __debug__:
            assert ret != None
        return ret

    def isnull(self):
        return False

    def eval(self, args, ldict):
        if str(self) in ldict:
            #this is ignoring the parens...
            ldict[str(self)].base.eval(args, ldict)
        else:
            if str(args.base) in args.control.delims['applier']:
                if __debug__:
                    assert len(args) > 0, "No known Obj function '{}' for Obj '{}'!".format(args, self)
                name = str(args[0])
                if name == 'copy':
                    ldict.last = ldict.last.deepcopy()
                if name == 'type':
                    ldict.last.base = ldict.last.base.objtype
                else:
                    raise SyntaxError("No known Obj function '{}' for Obj '{}'!".format(args, self))
            else:
                if __debug__:
                    assert args.base is self, "The argument's base ({}) isn't this base ({}) !".format(args.base, self.base)
                ldict.last = args.deepcopy()


    def deepcopy(self):
        return copy.deepcopy(self)

    def __bool__     (self): return bool(self.base)
    def _func_add    (self, other): return self.base +  other.base
    def _func_sub    (self, other): return self.base -  other.base
    def _func_mul    (self, other): return self.base *  other.base
    def _func_div    (self, other): return self.base /  other.base
    def _func_mod    (self, other): return self.base %  other.base
    def _func_pow    (self, other): return self.base ** other.base
    def _func_and    (self, other): return self.base &  other.base
    def _func_xor    (self, other): return self.base ^  other.base
    def _func_or     (self, other): return self.base |  other.base
    def _func_lshift (self, other): return self.base << other.base
    def _func_rshift (self, other): return self.base >> other.base
    def _func_eq     (self, other): return self.base == other.base
    def _func_ne     (self, other): return self.base != other.base
    def _func_gt     (self, other): return self.base >  other.base
    def _func_ge     (self, other): return self.base >= other.base
    def _func_lt     (self, other): return self.base <  other.base
    def _func_le     (self, other): return self.base <= other.base


    def updatebase(self, other, fname):
        ret = str(self)
        if   fname == '': self.base = other.base
        elif fname == '+': self.base += other.base
        elif fname == '-': self.base -= other.base
        elif fname == '*': self.base *= other.base
        elif fname == '/': self.base /= other.base
        elif fname == '%': self.base %= other.base
        elif fname == '**': self.base **= other.base
        elif fname == '&': self.base &= other.base
        elif fname == '^': self.base ^= other.base
        elif fname == '|': self.base |= other.base
        elif fname == '>': self.base >>= other.base
        elif fname == '<': self.base <<= other.base
        else: raise SyntaxError("Unknown updatebase function '{}'!".format(fname))
        return ret