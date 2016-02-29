class obj():
    """
    The base class for all of the objects.
    """

    #used to translate from symbols to functions.
    def __init__(self, base):
        if __debug__:
            assert not isinstance(base, obj), type(base) #only allowed to pass non-objs
        self.base = base

    def __repr__(self):
        return 'obj({})'.format(self.base)

    def __str__(self):
        return str(self.base)

    def scrubstr(self, control):
        return str(self)
    @staticmethod
    def frombase(ele, control):
        """
        Used when passing a string to determine which base to use.
        """
        if isinstance(ele, obj):
            return ele
        if ele == None:
            from Objects.NullObj import nullobj
            return nullobj()
        if __debug__:
            assert isinstance(ele, str), type(ele) #can only read strs. otherwise, use appropriate subclass.
        if ele in control.allkws:
            return control.allkws[ele]
        from Objects.NumObj import numobj
        ret = numobj.frombase(ele, control)
        if ret == None:
            from Objects.StrObj import strobj
            ret = strobj.frombase(ele, control)
            if ret == None:
                ret = obj(ele)
        if __debug__:
            assert ret != None
        return ret

    def isnull(self):
        from Objects.NullObj import nullobj
        return isinstance(self, nullobj)

    def eval(self, args, ldict):
        if str(self) in ldict:
            #this is ignoring the parens...
            ldict[str(self)].base.eval(args, ldict)
        else:
            if __debug__:
                assert args.base is self, "The argument's base ({}) isn't this base ({}) !".format(args.base, self.base)
            print(args.base)
            ldict.lastval = args

    def copybase(self):
        import copy
        return copy.deepcopy(self.base)

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


    def updatebase(self, other, funcname, ldict):
        ret = str(self)
        self.base = other.base
        return ret




























