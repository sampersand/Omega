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
    ldict.last = args.newgroup(dictobj(ldict.deepcopy()))
    del ldict.last.base.base.last

def _itos(self, args, ldict):
    #args 0 is itos
    if __debug__:
        assert str(args[0]) == 'itos', "... how was it passed if the first argument wasn't this function?"
        assert len(args[1]) == 1, 'om:itos:(string to convert,)'
    args[1][0].eval(ldict)
    ldict.last.base = strobj(str(ldict.last.base.base))
def _type(self, args, ldict):
    if __debug__:
        assert str(args[0]) == 'type', "... how was it passed if the first argument wasn't this function?"
        assert len(args[1]) == 1, 'om:type:(object to get type of,)' + repr(args[1])
    args[1][0].eval(ldict)
    ldict.last.base = typeobj(type(ldict.last.base))

_definedfuncs = {
    'rand' : _rand,
    'ldict': _ldict,
    'itos' : _itos,
    'type' : _type,
}











