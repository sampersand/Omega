import random
from Objects import floatobj, dictobj, strobj, typeobj
def eval(self, args, ldict):
    if __debug__:
        assert len(args) > 0, "currently '{}' doesn't support empty function calls!".format(self)
    name = str(args[0])
    if name not in _definedfuncs:
        raise SyntaxError("No known 'om' function '{}' with arguments '{}'!".\
                          format(name, '' if len(args) == 0 else args[1:]))
    else:
        _definedfuncs[name](self, args, ldict)

def _rand(self, args, ldict):
    ldict.last = args.newgroup(floatobj(random.random()))

def _ldict(self, args, ldict):
    ldict.last = args.newgroup(dictobj(ldict))
    del ldict.last.base.base.last

def _changetype(self, args, ldict):
    if __debug__:
        assert str(args[0]) == 'changetype', "... how was it passed if the first argument wasn't this function?"
        assert len(args[1]) == 2, 'om:changetype:(object to convert, type to convert it to)'
    args[1][1].eval(ldict)
    typ = ldict.last.base
    if __debug__:
        assert isinstance(typ, typeobj), "can only change an object's type by passing a type object!"
    args[1][0].eval(ldict)

    ldict.last.base = typ.base(typ.base.pytype(ldict.last.base.base))
def _type(self, args, ldict):
    if __debug__:
        assert str(args[0]) == 'type', "... how was it passed if the first argument wasn't this function?"
        assert len(args[1]) == 1, 'om:type:(object to get type of,)' + repr(args[1])
    args[1][0].eval(ldict)
    ldict.last.base = typeobj(type(ldict.last.base))

_definedfuncs = {
    'rand' : _rand,
    'ldict': _ldict,
    'changetype' : _changetype,
    'type' : _type,
}







