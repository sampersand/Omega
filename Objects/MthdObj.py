from Objects import obj
class mthdobj(obj):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return super().__repr__().replace(')', '%r)' % self.name)

class funcobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

class ufuncobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

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
                last = lcls.last
                arg.evalgrp(lcls)
                if __debug__:
                    assert hasattr(lcls.last.baseobj, self.attrstr),\
                        "cannot perform '{}' on '{}'!".format(self.attrstr, repr(arg.baseobj))
                assert 0,' todo'
                lcls.last = lcls.last.deepcopy()
                lcls.last.data = getattr(last.data, self.attrstr).__call__(lcls.last.data)
    def _speceval(self, args, lcls):
        ctrl = args.control
        if self.name in ctrl.delims:
            if self.name in ctrl.delims['applier']:
                args[0].evalgrp(lcls)
                lcls.last.baseobj.eval(args[1:], lcls)
            elif self.name in ctrl.delims['endline']:
                for arg in args:
                    arg.evalgrp(lcls)
                    if not lcls.ret.isnull():
                        del lcls.ret
                        break
    #     ctrl = args.control
    #     name = str(self)
    #     if name in ctrl.delims:
    #         if name in ctrl.delims['applier']:
    #             args[0].eval(lcls)
    #             lcls.last.data.eval(args[1:], lcls)
    #             return
    #         if name in ctrl.delims['endline']:
    #             for line in args: #each ';' is a line.
    #                 line.eval(lcls)
    #                 if not lcls.ret.data.isnull():
    #                     break
    #             return
    #         if name in ctrl.delims['arraysep']:
    #             l = args.newgroup(parens = args.parens)
    #             l.data = arrayobj()
    #             for ele in args:
    #                 ele.eval(lcls)
    #                 if not lcls.ret.data.isnull():
    #                     break
    #                 l.data.append(lcls.last)
    #             lcls.last = l
    #             return
    #     if name in ctrl.opers['binary']:
    #         if __debug__:
    #             assert name not in ctrl.opers['binary']['math'], 'all math should have a func associated!'
    #             assert name not in ctrl.opers['binary']['bitwise'], 'all bitwise should have a func associated!'
    #         if name in ctrl.opers['binary']['assignment']:
    #             d = name in args.control.opers['binary']['assignment']['r']
    #             args[d - 1].eval(lcls)
    #             for args in args[slice(d or None, d - 1 or None, None)]:
    #                 self._evalassign(args, lcls)
    #             return
    #         if name in ctrl.opers['binary']['logic']:
    #             pass
    #     raise SyntaxError("Unknown Special Operator '{}' in arguments '{}'! Known operators: {}".\
    #                       format(self, args, ctrl.allopers.keys()))
    # def _evalassign(self, args, lcls):
    #     if __debug__:
    #         assert str(self) in args.control.opers['binary']['assignment'],\
    #               "Cant evalassign when '%s' isnt assgn oper!" % self
    #     last = lcls.last
    #     args.eval(lcls)
    #     sname = str(self)[1:-1]
    #     lstr = str(lcls.last)
    #     if sname == '':
    #         if type(lcls.last.data) == obj: #aka, if it isn't a special object.
    #             lcls[lstr] = last
    #             lcls.last = lcls[lstr] #is deepcopy really required?
    #         else:
    #             lcls.last.data.updatedata(last.data, sname)
    #             # lcls.last = lcls.last.deepcopy() #is deepcopy really required?
    #     else:
    #         if type(lcls.last.data) == obj: #aka, if it isn't a special object.
    #             lcls[lstr] = last
    #             lcls.last = lcls[lstr] #is deepcopy really required?
    #         else:
    #             lcls.last.data.updatedata(last.data, sname)

















