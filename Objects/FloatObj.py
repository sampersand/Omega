from Objects import numobj, floatre
class floatobj(numobj):
    def __init__(self, base):
        if __debug__:
            assert isinstance(base, float), type(base)
        super().__init__(base)

    def __repr__(self):
        return 'floatobj({})'.format(self.base)

    def eval(self, args, ldict):
        try:
            super().eval(args, ldict)
        except SyntaxError:
            name = str(args[0])
            if name == 'round':
                from Objects import intobj
                ldict.last = args.newgroup(intobj(round(self.base)))

    @staticmethod
    def fromstr(base, control):
        ret = floatre.findall(base)
        if ret:
            if __debug__:
                assert len(ret) == 1 #there should onyl be 1 match!
                assert len(ret[0]) == 3 #should be (###)e(pos/neg)(###)
            ret = ret[0]
            ret = (ret[2] and '{}e{}{}'.format(ret[0], ret[1] in 'pP' and '+' or '-', ret[2]) or ret[0])
            # for some reason, '' in 'pP' is true.
        print(ret)
        return floatobj(float(ret)) if ret else None
