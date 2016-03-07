from Objects import collectionobj
class arrayobj(collectionobj):
    _pyobj = list
    def evalobj(self, args, lcls):
        if super().evalobj(args, lcls) == NotImplemented:
            for arg in args:
                arg.evalgrp(lcls)