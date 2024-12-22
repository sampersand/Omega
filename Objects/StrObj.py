from Objects import obj

class strobj(obj):
    _pyobj = str

    ## MODIFICATION, 2024-12-22, added this function in (previously you couldn't actually _do_ anything with strings)
    def _evalargs(self, args, lcls, ignore):
        from Group import group
        ret = super()._evalargs(args, lcls, ignore)
        if ret != NotImplemented:
            return ret

        fncname = str(args[0])
        from Objects import intobj, strobj

        if fncname == 'len':
            lcls.iv.last = group(
                data=len(lcls.iv.last.data), baseobj = intobj(), control=args.control)
        elif fncname == '$int':
            lcls.iv.last = group(
                data=int(lcls.iv.last.data), baseobj=intobj(), control=args.control)
        elif fncname == 'substr':
            last = str(lcls.iv.last.data)
            args[1][0].evalgrp(lcls)
            start = int(lcls.iv.last.data)
            args[1][1].evalgrp(lcls)
            length = int(lcls.iv.last.data)

            lcls.iv.last = group(data=last[start:start+length], baseobj=strobj(), control=args.control)
        else:
            raise SyntaxError("No known '{}' function '{}'!".format(type(self).__qualname__, fncname))

