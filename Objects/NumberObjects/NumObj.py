from Objects import obj
class numobj(obj):
    def evalobj(self, args, lcls):
        if super().evalobj(args, lcls) != NotImplemented:
            return
        assert 0, repr(args)