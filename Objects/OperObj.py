from Objects.FuncObj import funcobj
class operobj(funcobj):
    """
    The class that represents operators on objects.
    """
    def __init__(self, base, priority):
        super().__init__(base, None)
        self.priority = priority

    def __repr__(self):
        return 'operobj({},{})'.format(self.base, self.priority)

    def eval(self, args, ldict):
        ctrl = args.control
        name = str(self)
        if __debug__:
            assert name in ctrl.opers, "'{}' should be in opers!".format(self)
            assert self is args.base, 'just noticed this, not a hard and fast rule...'
        if name in ctrl.delims:
            if name in ctrl.delims['endline']:
                for line in args: #each ';' is a line.
                    if not line.base.isnull():
                        line.eval(ldict)
                    if ldict.hasret():
                        break
                return
        elif name in ctrl.opers['binary']:
            if name in ctrl.opers['binary']['math']:
                args[0].eval(ldict)
                for arg in args[1:]:
                    ldict.lastval.base._evalmath(arg, self, ldict)
                return
            elif name in ctrl.opers['binary']['logic']:
                pass
            elif name in ctrl.opers['binary']['bitwise']:
                pass
            elif name in ctrl.opers['binary']['assignment']:
                d = name in args.control.opers['binary']['assignment']['r']
                args[d - 1].eval(ldict)
                for arg in args[slice(d or None, d - 1 or None, None)]:
                    self._evalassign(arg, ldict)
                return
        raise SyntaxError("Unknown Operator '{}' in arguments '{}'! Known operators: {}".format(self, args, 
                                                                                                ctrl.allopers.keys()))
    def _evalassign(self, args, ldict):
        if __debug__:
            assert str(self) in args.control.opers['binary']['assignment'],\
                  "Cant evalassign when '%s' isnt assgn oper!" % self
        last = ldict.lastval
        elestr = str(args)
        sname = str(self)[1:-1]
        if sname == '':
            ldict[elestr] = last
            ldict.lastval = ldict[elestr].deepcopy()
        else:
            assert 0, "iopers aren't supported yet!"

















