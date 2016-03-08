from Objects import collectionobj
class arrayobj(collectionobj):
    _pyobj = list
    def evalobj(self, args, lcls):
        try:
            super().evalobj(args, lcls):
        except SyntaxError:
            for arg in args:
                arg.evalgrp(lcls)