from Objects import collectionobj, intobj
class arrayobj(collectionobj):
    _pyobj = list
    def evalobj(self, args, lcls):
        # ret = super().evalobj(args, lcls)
        # if ret != NotImplemented:
            # return ret
        for arg in args:
            arg.evalgrp(lcls)
# def evalobj(self, args, lcls):
#     ret = super().evalobj(args, lcls, docopy = False)
#     print('ret:',ret,'@')
#     if ret == 0:
#         for arg in args:
#             arg.evalgrp(lcls)
#         return lcls.iv.last
#         assert 0, lcls.iv.last
#     if ret == NotImplemented: #this calls super()._evalargs twice. once here, once in self._evalargs
#         self._evalargs(args, lcls)
#     return ret
# def _evalargs(self, args, lcls):
#     ret = super()._evalargs(args, lcls)
#     if ret != NotImplemented:
#         return ret
#     name = "_" + str(args[0])
#     if name not in dir(self):
#         if type(self) == arrayobj:
#             raise ValueError("Function '{}' isn't defined yet!".format(str(args[0])))
#         return NotImplemented
#     self.__getattribute__(name)(args[1:], lcls)

# def _get(self, args, lcls):
#     if __debug__:
#         assert len(args) == 1, 'arr:get:(pos)'
#         assert len(args[0]) == 1, 'arr:get:(pos)'
#         assert isinstance(args[0].baseobj, arrayobj), 'have to pass an array as a parameter!'
#     last = lcls.iv.last
#     args[0][0].evalgrp(lcls)
#     lcls.iv.last = last[int(lcls.iv.last.data)]

# def _len(self, args, lcls):
#     if __debug__:
#         assert len(args) == 0, 'arr:len'
#     from Group import group
#     lcls.iv.last = group(data = str(len(lcls.iv.last)), baseobj = intobj(), control = args.control)

# def _pop(self, args, lcls):
#     if __debug__:
#         assert len(args) == 1, 'arr:pop:(pos)'
#         assert len(args[0]) <= 1, 'arr:pop:[pos]' #[] is optional, () is required
#         assert isinstance(args[0].baseobj, arrayobj), 'have to pass an array as a parameter!'
#     last = lcls.iv.last
#     if len(args[0]) == 0:
#         pos = -1
#     else:
#         args[0][0].evalgrp(lcls)
#         int(lcls.iv.last.data)
#     lcls.iv.last = last[pos].deepcopy()
#     del last[pos]

