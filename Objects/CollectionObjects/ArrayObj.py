from Objects import collectionobj
class arrayobj(collectionobj):
    _pyobj = list
    def evalobj(self, args, lcls, iflcls = True, docopy = True, throwfunc = True):
        if super().evalobj(args, lcls, throwfunc = False) == None:
            return
        for arg in args:
            arg.evalgrp(lcls)