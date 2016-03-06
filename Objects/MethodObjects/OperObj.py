from Objects import mthdobj, obj
class operobj(mthdobj):
    def __init__(self, name, priority, attrstr):
        """ name is used to print, attrstr is used to actually execute the function. """
        super().__init__(name)
        self.priority = priority
        self.attrstr = attrstr
    def __repr__(self):
        return super().__repr__().replace(')', ', %r, %r)' % (self.priority, self.attrstr))
    def evalobj(self, args, lcls):
        if __debug__:
            assert args.datastr in args.control.opers, "'{}' should be in opers!".format(self)
        if self.attrstr == None:
            self._speceval(args, lcls)
        else:
            args[0].evalgrp(lcls)
            for arg in args[1:]:
                last = lcls.iv.last
                arg.evalgrp(lcls)
                if __debug__:
                    assert last is not lcls.iv.last, type(arg.baseobj)
                if __debug__:
                    assert hasattr(last.baseobj, self.attrstr),\
                        "cannot perform '{}' on '{}'!".format(self.attrstr, repr(last.baseobj))
                lcls.iv.last = lcls.iv.last.deepcopy()
                lcls.iv.last.data = getattr(last.baseobj, self.attrstr).__call__(last, lcls.iv.last)
    def _speceval(self, args, lcls):
        ctrl = args.control
        if self.name in ctrl.delims:
            if self.name in ctrl.delims['applier']:
                args[0].evalgrp(lcls)
                lcls.iv.last.baseobj.evalobj(args[1:], lcls)
                return
            if self.name in ctrl.delims['endline']:
                for arg in args:
                    arg.evalgrp(lcls)
                    if lcls.iv.ret:
                        del lcls.iv.ret
                        break
                return
            if self.name in ctrl.delims['arraysep']:
                assert 0, 'todo: arraysep'
                # l = args.newgroup(parens = args.parens)
                # l.data = arrayobj()
                # for ele in args:
                #     ele.evalevalgrp(lcls)
                #     if lcls.ret.data:
                #         break
                #     l.data.append(lcls.iv.last)
                # lcls.iv.last = l
                # return
            
        if self.name in ctrl.opers['binary']:
            if __debug__:
                assert self.name not in ctrl.opers['binary']['math'], 'all math should have a func associated!'
                assert self.name not in ctrl.opers['binary']['bitwise'], 'all bitwise should have a func associated!'
            if self.name in ctrl.opers['binary']['assignment']:
                d = self.name in args.control.opers['binary']['assignment']['r']
                args[d - 1].evalgrp(lcls)
                for arg in args[slice(d or None, d - 1 or None, None)]:
                    self._evalassign(arg, lcls)
                return
            if self.name in ctrl.opers['binary']['logic']:
                pass
        raise SyntaxError("Unknown Special Operator '{}' in arguments '{}'! Known operators: {}".\
                          format(self, args, ctrl.allopers.keys()))
    def _evalassign(self, args, lcls):
        if __debug__:
            assert self.name in args.control.opers['binary']['assignment'],\
                  "Cant evalassign when '%s' isnt assgn oper!" % self
        print(repr(lcls),"@")
        last = lcls.iv.last
        args.evalgrp(lcls)
        if __debug__:
            assert last is not lcls.iv.last, type(args.baseobj)
        sname = self.name[1:-1]
        lstr = str(lcls.iv.last)
        if sname == '':
            if type(lcls.iv.last.baseobj) == obj: #aka, if it isn't a special object.
                lcls[lstr] = last
                lcls.iv.last = lcls[lstr] #is deepcopy really required?
            else:
                lcls.iv.last.data.updatedata(last.data, sname)
                # lcls.iv.last = lcls.iv.last.deepcopy() #is deepcopy really required?
        else:
            if type(lcls.iv.last.data) == obj: #aka, if it isn't a special object.
                lcls[lstr] = last
                lcls.iv.last = lcls[lstr] #is deepcopy really required?
            else:
                lcls.iv.last.data.updatedata(last.data, sname)













