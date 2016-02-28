class obj():
    """
    The base class for all of the objects.
    """
    def __init__(self, base):
        if __debug__:
            assert not isinstance(base, obj), type(base) #only allowed to pass non-objs
        self.base = base

    def __repr__(self):
        return 'obj({})'.format(self.base)

    def __str__(self):
        return str(self.base)

    @staticmethod
    def frombase(ele, control):
        """
        Used when passing a string to determine which base to use.
        """
        if isinstance(ele, obj):
            return ele
        if ele == None:
            return nullobj()
        if __debug__:
            assert isinstance(ele, str), type(ele) #can only read strs. otherwise, use appropriate subclass.
        if ele in control.allkws:
            return control.allkws[ele]
        ret = numobj.fromstr(ele)
        if ret == None:
            ret = strobj.fromstr(ele)
            if ret == None:
                ret = obj(ele)
        if __debug__:
            assert ret != None
        return ret

    def isnull(self):
        return isinstance(self, nullobj)

    def eval(self, args, ldict):
        if str(self) in ldict:
            #this is ignoring the parens...
            ldict[str(self)].base.eval(args, ldict)
        else:
            if __debug__:
                assert args.base is self, "The argument's base ({}) isn't this base ({}) !".format(args.base, self.base)
            ldict.lastvalue = args

