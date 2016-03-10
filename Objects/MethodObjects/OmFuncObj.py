from Objects import funcobj, typeobj
from Group import group
import random
class omfuncobj(funcobj):
    def __init__(self, name = ''):
        super().__init__(name)

    def _evalargs(self, args, lcls):
        #exact same code as funcobj, except name is args.data
        ret = super()._evalargs(args, lcls)
        if ret != NotImplemented:
            return ret
        if __debug__:
            assert len(args) > 0, "'Only can have length of 1 currently, not '{}'".format(args)
        name = "_" + args[0].data
        if name not in dir(self):
            # if type(self) == funcobj:
            raise ValueError("Function '{}' isn't defined yet!".format(name))
        self.__getattribute__(name)(args[1:], lcls)
    # def evalobj(self, args, lcls, iflcls = True, docopy = True, throwfunc = True):
    #     #exact same code as funcobj, except name is args.data
    #     if super().evalobj(args, lcls, throwfunc = False) == None:
    #         return
    #     if __debug__:
    #         assert len(args) == 1, "'Only can have length of 1 currently, not '{}'".format(args)
    #     name = "_" + args[0].data
    #     if name not in dir(self):
    #         if type(self) == funcobj:
    #             raise ValueError("Function '{}' isn't defined yet!".format(self.name))
    #         return 0
    #     self.__getattribute__(name)(args, lcls)

    def _rand(self, args, lcls):
        lcls.iv.last = group(data = str(random.random()), control = args.control)

    def _types(self, args, lcls):
        if __debug__:
            assert len(args) in {1, 2}, "om:types:(TYPE)[:(init args)], not " + str(args)
        base = args[0].datastr
        from Objects import __all__ as allobj
        if __debug__:
            assert base in allobj, "No such type of '{}'!".format(base)
        topassobj = __import__('Objects').__getattribute__(base)
        lcls.iv.last = group(data = str(topassobj), baseobj = typeobj(\
            baseclass = group(baseobj = topassobj(), control = args.control)), control = args.control)














