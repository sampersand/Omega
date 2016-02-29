from Objects import numobj, decre, binre, hexre, octre, unire, nbases
class intobj(numobj):
    def __init__(self, base, nbase = 10):
        if __debug__:
            assert isinstance(base, int), type(base)
        super().__init__(base)
        self.nbase = nbase 
    def __repr__(self):
        return 'intobj({}{})'.format(self.base, '' if self.nbase == 10 else 'nbase='+str(self.nbase))

    @staticmethod
    def frombase(base, control):
        ret = decre.findall(base)
        if not ret:
            ret = binre.findall(base)
            if not ret:
                ret = hexre.findall(base)
                if not ret:
                    ret = octre.findall(base)
        if ret:
            ret = (nbases[ret[0][0].lower()], ret[0][1])
        if not ret:
            ret = unire.findall(base)
            if ret:
                ret = (int(ret[0][0]), ret[0][1])
        if ret:
            ret = (int(ret[1], ret[0]), ret[0])
        if __debug__:
            assert not ret or len(ret) == 2 #only 1 or 0 matches
        return intobj(ret[0], ret[1]) if ret else None 
