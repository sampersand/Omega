from Objects import mthdobj, obj, arrayobj, typeobj
import Objects
from Group import group
class operobj(mthdobj):
    def __init__(self, name, priority, attrstr):
        """ name is used to print, attrstr is used to actually execute the function. """
        super().__init__(name)
        self.priority = priority
        self.attrstr = attrstr

    def __repr__(self):
        return super().__repr__().replace(')', ', %r, %r)' % (self.priority, self.attrstr))

    @classmethod
    def _type_for(cls, obj):
        if isinstance(obj.data, str): return Objects.strobj()
        if isinstance(obj.data, int): return Objects.intobj()
        if isinstance(obj.data, float): return Objects.floatobj()
        if isinstance(obj.data, complex): return Objects.complexobj()
        if isinstance(obj.data, bool): return Objects.boolobj()
        if isinstance(obj.data, list): return Objects.arrayobj()
        if isinstance(obj.data, dict): return Objects.dictobj()

    def evalobj(self, args, lcls):
        #todo: this
        if self.attrstr == None:
            self._speceval(args, lcls)
        else:
            args[0].evalgrp(lcls)
            for arg in args[1:]:
                last = lcls.iv.last.deepcopy()
                arg.evalgrp(lcls)
                if __debug__:
                    assert last is not lcls.iv.last, type(arg.baseobj)
                if __debug__:
                    assert hasattr(last.baseobj, self.attrstr),\
                        "cannot perform '{}' on '{}'!".format(self.attrstr, repr(last.baseobj))
                lcls.iv.last = lcls.iv.last.deepcopy()
                lcls.iv.last.data = getattr(last.baseobj, self.attrstr).__call__(last, lcls.iv.last)
                kind = operobj._type_for(lcls.iv.last)
                if kind:
                    lcls.iv.last.baseobj = kind

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
                        # del lcls.iv.ret
                        break
                return
            if self.name in ctrl.delims['arraysep']:
                grp = group(baseobj = arrayobj(), parens = args.parens, control = args.control)
                for arg in args:
                    arg.evalgrp(lcls)
                    if lcls.iv.ret.data:
                        break
                    grp.append(lcls.iv.last)
                lcls.iv.last = grp
                return
                # assert 0, 'todo: arraysep'
            
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
        last = lcls.iv.last
        lcls.iv.last = args
        if __debug__:
            assert last is not lcls.iv.last, type(args.baseobj)
        sname = self.name[1:-1]
        name = str(lcls.iv.last.data)
        if sname:
            args.evalgrp(lcls)
            args.control.opers['binary']['math'][sname].evalobj([lcls.iv.last, last], lcls)
            last = lcls.iv.last
        lcls[name] = last






















