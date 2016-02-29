from Objects import numobj
class intobj(numobj):
    import re
    decre = re.compile(r'^(?:0([dD]))?(\d+)I?$')    #can have 'I' at the end
    binre = re.compile(r'^0([bB])([01]+)I?$')       #can have 'I' at the end
    hexre = re.compile(r'^0([xX])([\dA-Fa-f]+)I?$') #can have 'I' at the end
    octre = re.compile(r'^0([oO])([0-7]+)I?$')      #can have 'I' at the end
    unire = re.compile(r'^0[uU](\d+)[uU](\d+)I?$')  #can have 'I' at the end

    nbases = {'d':10, '':10, 'b':2, 'x':16, 'o':8}
    def __init__(self, base, nbases = 10):
        if __debug__:
            assert isinstance(base, int), type(base)
        super().__init__(base)
        self.nbases = nbases 
    def __repr__(self):
        return 'intobj({}{})'.format(self.base, '' if self.nbases == 10 else 'nbases='+str(self.nbases))

    @staticmethod
    def frombase(base, control):
        ret = intobj.decre.findall(base)
        if not ret:
            ret = intobj.binre.findall(base)
            if not ret:
                ret = intobj.hexre.findall(base)
                if not ret:
                    ret = intobj.octre.findall(base)
        if ret:
            ret = (intobj.nbases[ret[0][0].lower()], ret[0][1])
        if not ret:
            ret = intobj.unire.findall(base)
            if ret:
                ret = (int(ret[0][0]), ret[0][1])
        if ret:
            ret = (int(ret[1], ret[0]), ret[0])
        if __debug__:
            assert not ret or len(ret) == 2 #only 1 or 0 matches
        return intobj(ret[0], ret[1]) if ret else None 
