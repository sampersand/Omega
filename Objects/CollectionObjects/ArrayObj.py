from Objects import collectionobj
class arrayobj(collectionobj):
    _pyobj = list
    # def evalobj(self, args, lcls):
    #     # ret = super().evalobj(args, lcls)
    #     # if ret != NotImplemented:
    #         # return ret
    #     for arg in args:
    #         arg.evalgrp(lcls)
    def evalobj(self, args, lcls):
        ret = super().evalobj(args, lcls)
        if ret == 0:
            for arg in args:
                arg.evalgrp(lcls)
        if ret == NotImplemented: #this calls super()._evalargs twice. once here, once in self._evalargs
            self._evalargs(args, lcls)
    def _evalargs(self, args, lcls):
        ret = super()._evalargs(args, lcls)
        if ret != NotImplemented:
            return ret
        name = "_" + str(args[0])
        if name not in dir(self):
            if type(self) == arrayobj:
                raise ValueError("Function '{}' isn't defined yet!".format(str(args[0])))
            return NotImplemented
        self.__getattribute__(name)(args[1:], lcls)
    def _get(self, args, lcls):
        if __debug__:
            assert len(args) == 1, 'can only get a single position!'
            assert len(args[0]) == 1, 'can only get a single position!'
            assert isinstance(args[0].baseobj, arrayobj), 'have to pass an array as a parameter!'
        last = lcls.iv.last
        args[0][0].evalgrp(lcls)
        from Group import group
        lcls.iv.last = last[int(lcls.iv.last.data)]
