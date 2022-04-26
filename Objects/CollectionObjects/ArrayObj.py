from Objects import collectionobj, intobj

class arrayobj(collectionobj):
    _pyobj = list
    # def evalobj(self, args, lcls):
    #     ret = super().evalobj(args, lcls)
    #     if ret != NotImplemented:
    #         return ret
    #     for arg in args:
    #         arg.evalgrp(lcls)
    def evalobj(self, args, lcls):
        ret = super().evalobj(args, lcls, docopy = False)
        if ret == 0:
            for arg in args:
                arg.evalgrp(lcls)
            return lcls.iv.last
        if ret == NotImplemented: #this calls super()._evalargs twice. once here, once in self._evalargs
            self._evalargs(args, lcls)
        return ret
    def _evalargs(self, args, lcls, ignore):
        ret = super()._evalargs(args, lcls, ignore)
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
            assert len(args) == 1, 'arr:get:(pos)'
            assert len(args[0]) == 1, 'arr:get:(pos)'
            assert isinstance(args[0].baseobj, arrayobj), 'have to pass an array as a parameter!'
        last = lcls.iv.last
        args[0][0].evalgrp(lcls)
        lcls.iv.last = last[int(lcls.iv.last.data)]

    def _set(self, args, lcls):
        if __debug__:
            assert len(args) == 1, 'arr:set:(pos, ele)'
            assert len(args[0]) == 2, 'arr:set:(pos, ele)'
        last = lcls.iv.last
        args[0].evalgrp(lcls)
        args = lcls.iv.last
        args[0].evalgrp(lcls)
        idx = int(lcls.iv.last.data)
        args[1].evalgrp(lcls)
        last[idx] = lcls.iv.last

    def _add(self, args, lcls):
        from Group import group

        if __debug__:
            assert len(args) == 1, 'arr:add:(ary)'
            assert len(args[0]) == 1, 'arr:add:(ary)'
            assert isinstance(args[0].baseobj, arrayobj), 'have to pass an array as a parameter!'
        last = lcls.iv.last.deepcopy()
        args[0][0].evalgrp(lcls)

        last += list(lcls.iv.last)
        lcls.iv.last = last

    def _len(self, args, lcls):
        from Group import group
        if __debug__:
            assert len(args) == 0, 'arr:len'
        lcls.iv.last = group(data = str(len(lcls.iv.last)), baseobj = intobj(), control = args.control)

    def _push(self, args, lcls):
        if __debug__:
            assert len(args) == 1, 'arr:add:(ele)'
            assert len(args[0]) == 1, 'arr:add:(ele)'
            assert isinstance(args[0].baseobj, arrayobj), 'have to pass an array as a parameter!'
        last = lcls.iv.last
        args[0][0].evalgrp(lcls)
        last.append(lcls.iv.last)
        lcls.iv.last = last


    def _pop(self, args, lcls):
        if __debug__:
            assert len(args) == 1, 'arr:pop:(pos)'
            assert len(args[0]) <= 1, 'arr:pop:[pos]' #[] is optional, () is required
            assert isinstance(args[0].baseobj, arrayobj), 'have to pass an array as a parameter!'
        last = lcls.iv.last
        if len(args[0]) == 0:
            pos = -1
        else:
            args[0][0].evalgrp(lcls)
            int(lcls.iv.last.data)
        lcls.iv.last = last[pos].deepcopy()
        del last[pos]

