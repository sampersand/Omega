from Objects import arrayobj, obj, methodobj
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
                last = ldict.last
                arg.eval(ldict)
                if __debug__:
                    assert hasattr(ldict.last.base, self.attrstr),\
                        "cannot perform '{}' on '{}'!".format(self.attrstr, repr(arg))
                ldict.last = ldict.last.deepcopy()
                ldict.last.base.base = getattr(last.base, self.attrstr).__call__(ldict.last.base)
    def _speceval(self, args, ldict):
        ctrl = args.control
        name = str(self)
        if name in ctrl.delims:
            if name in ctrl.delims['endline']:
                for line in args: #each ';' is a line.
                    if not line.base.isnull():
                        line.eval(ldict)
                    if not ldict.ret.base.isnull():
                        break
            elif name in ctrl.delims['arraysep']:
                l = args.newgroup(parens = args.parens)
                l.base = arrayobj()
                for ele in args:
                    if not ele.base.isnull():
                        ele.eval(ldict)
                    if not ldict.ret.base.isnull():
                        break
                    l.base.base.append(ldict.last)
                ldict.last = l
            elif name in ctrl.delims['applier']:
                args[0].eval(ldict)
                ldict.last.base.eval(args[1:], ldict)
        elif name in ctrl.opers['binary']:
            if __debug__:
                assert name not in ctrl.opers['binary']['math'], 'all math should have a func associated!'
                assert name not in ctrl.opers['binary']['bitwise'], 'all bitwise should have a func associated!'
            if name in ctrl.opers['binary']['logic']:
                raise SyntaxError("Unknown Special Operator '{}' in arguments '{}'! Known operators: {}".format(self, args, 
                                                                                                ctrl.allopers.keys()))
            elif name in ctrl.opers['binary']['assignment']:
                d = name in args.control.opers['binary']['assignment']['r']
                args[d - 1].eval(ldict)
                for arg in args[slice(d or None, d - 1 or None, None)]:
                    self._evalassign(arg, ldict)
        else:
            raise SyntaxError("Unknown Special Operator '{}' in arguments '{}'! Known operators: {}".format(self, args, 
                                                                                                ctrl.allopers.keys()))
    def _evalassign(self, args, ldict):
        if __debug__:
            assert str(self) in args.control.opers['binary']['assignment'],\
                  "Cant evalassign when '%s' isnt assgn oper!" % self
        last = ldict.last
        args.eval(ldict)
        sname = str(self)[1:-1]
        if sname == '':
            if type(ldict.last.base) == obj: #aka, if it isn't a special object.
                ldict[str(ldict.last)] = last
                ldict.last = ldict[str(ldict.last)] #is deepcopy really required?
            else:
                ldict.last.base.updatebase(last.base, sname)
                ldict.last = ldict.last.deepcopy() #is deepcopy really required?
        else:
            if type(ldict.last.base) == obj: #aka, if it isn't a special object.
                ldict[str(ldict.last)] = last
                ldict.last = ldict[str(ldict.last)] #is deepcopy really required?
            else:
                ldict.last.base.updatebase(last.base, sname)
            # ldict.last = ldict.last.deepcopy() #is deepcopy really required?
            # print(repr(ldict.last.base))
            # assert 0, "iopers aren't supported yet!"
            # if argstr not in ldict:
            #     ldict[argstr] = ldict.last
            #     ldict.last = ldict.last.deepcopy()
            # else:
            #     args.newgroup(base = args.control.allopers[sname],\
            #           args = [ldict[argstr], last]).eval(ldict)
            #     ldict[argstr] = ldict.last.deepcopy()
            #     ldict[argstr] = ldict.last


















