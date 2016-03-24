from Objects import obj
class nullobj(obj):
    def __init__(self, isuser = False):
        self.isuser = isuser
    def _func_eq(self, obj1, obj2):
            return isinstance(obj1.baseobj, nullobj) and isinstance(obj2.baseobj, nullobj)