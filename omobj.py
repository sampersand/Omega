class omobj:
    def __init__(self, base, evalfunc = None):
        self.base = base
        self.evalfunc = evalfunc
    def __str__(self):
        return str(self.base)
    def __repr__(self):
        return 'omobj({},evalfunc={})'.format(repr(self.base), repr(self.evalfunc))
    def __bool__(self):
        return bool(str(self))
    def eval(self, grp, locls):
        print('attempting to eval grp \'{}\' with locls \'{}\' in omobj \'{}\''.format(grp, locls, self))
        if self.evalfunc == None:
            print('evalfunc is none, returning self.base ({})'.format(self.base))
            locls['$'] = self.base
            return
        print('its not none, but idk waht to do, so returning None')
        return None

class oper(omobj):

    def __init__(self, base, priority, evalfunc):
        super().__init__(base, evalfunc)
        self.priority = priority

    def __repr__(self):
        return 'oper({},{},{})'.format(self.base, self.priority, self.evalfunc)

    def __str__(self):
        return self.base
    def __lt__(self, other):
        return self.priority < other.priority

    def eval(self, grp, locls):
        print('attempting to eval grp \'{}\' with locls \'{}\' in oper \'{}\''.format(grp, locls, self))
        if self.evalfunc == None:
            print('evalfunc is none, returning self.base ({})'.format(self.base))
            locls['$'] = self.base

            return
        print("evaluating '{}' with locals {}".format(grp, locls))
        locls['$'] = self.evalfunc(grp, locls)
        print("evaluated '{}' with locals {}, and getting {}".format(grp, locls, locls['$']))

class func(omobj):
    def __init__(self, base):
        super().__init__(base, None)
    def eval(self, grp, locls):
        print('attempting to eval grp \'{}\' with locls \'{}\' in func \'{}\''.format(grp, locls, self))
        if self.evalfunc == None:
            print('evalfunc is none, returning self.base ({})'.format(self.base))
            return self.base
        return None