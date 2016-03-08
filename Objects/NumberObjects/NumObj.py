from Objects import obj
class numobj(obj):
    def evalobj(self, args, lcls):
        if super().evalobj(args, lcls) == None:
            return
        assert 0, repr(args)