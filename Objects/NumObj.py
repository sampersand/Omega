from Objects import obj
class numobj(obj):
    def evaluate(self, arg, lcls):
        pass
class intobj(numobj):
    pass
class floatobj(numobj):
    pass
class complexobj(floatobj):
    pass
class boolobj(intobj):
    pass