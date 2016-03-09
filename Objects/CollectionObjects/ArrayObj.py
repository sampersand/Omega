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
        name = "_" + self.name
        if name not in dir(self):
            if type(self) == funcobj:
                raise ValueError("Function '{}' isn't defined yet!".format(self.name))
            return NotImplemented
        self.__getattribute__('_' + self.name)(args, lcls)
        