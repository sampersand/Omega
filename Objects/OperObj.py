from Objects.MethodObj import methodobj
class operobj(methodobj):
    """
    The class that represents operators on objects.
    """
    def __init__(self, base, priority, attrstr):
        super().__init__(base, None)
        self.priority = priority
        self.attrstr = attrstr

    def __repr__(self):
        return 'operobj({},{},{})'.format(self.base, self.priority, self.attrstr)

    def eval(self, args, ldict):
        if __debug__:
            assert str(self) in args.control.opers, "'{}' should be in opers!".format(self)
            assert self is args.base, 'just noticed this, not a hard and fast rule...'
        if self.attrstr == None:
            self._speceval(args, ldict)
        else:
            args[0].eval(ldict)
            for arg in args[1:]:
                last = ldict.lastval
                arg.eval(ldict)
                if __debug__:
                    assert hasattr(ldict.lastval.base, self.attrstr),\
                        "cannot perform '{}' on '{}'!".format(self.attrstr, repr(arg))
                ldict.lastval = ldict.lastval.deepcopy()
                ldict.lastval.base.base = getattr(last.base, self.attrstr).__call__(ldict.lastval.base)
            return
    def _speceval(self, args, ldict):
        ctrl = args.control
        name = str(self)
        if name in ctrl.delims:
            if name in ctrl.delims['endline']:
                for line in args: #each ';' is a line.
                    if not line.base.isnull():
                        line.eval(ldict)
                    if ldict.hasret():
                        break
                return
            elif name in ctrl.delims['arraysep']:
                from Group import group
                l = group(parens = args.parens)
                from Objects import arrayobj
                l.base = arrayobj()
                for ele in args:
                    if not ele.base.isnull():
                        ele.eval(ldict)
                    if ldict.hasret():
                        break
                    l.base.base.append(ldict.lastval)
                ldict.lastval = l
                return
            elif name in ctrl.delims['applier']:
                args[0].eval(ldict)
                ldict.lastval.base.eval(args[1:], ldict)
                return
        elif name in ctrl.opers['binary']:
            if __debug__:
                assert name not in ctrl.opers['binary']['math'], 'all math should have a func associated!'
                assert name not in ctrl.opers['binary']['bitwise'], 'all bitwise should have a func associated!'
            if name in ctrl.opers['binary']['logic']:
                pass
            elif name in ctrl.opers['binary']['assignment']:
                d = name in args.control.opers['binary']['assignment']['r']
                args[d - 1].eval(ldict)
                for arg in args[slice(d or None, d - 1 or None, None)]:
                    self._evalassign(arg, ldict)
                return
        raise SyntaxError("Unknown Special Operator '{}' in arguments '{}'! Known operators: {}".format(self, args, 
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

















