import random
from Objects import floatobj, dictobj
def eval(self, args, ldict):
    if __debug__:
        assert len(args) > 0, "currently '{}' doesn't support empty function calls!".format(self)
    name = str(args[0])
    if name not in _definedfuncs:
        raise SyntaxError("No known 'om' function '{}' with arguments '{}'!".\
                          format(name, '' if len(args) == 0 else args[1:]))
    else:
        _definedfuncs[name](self, args[1:], ldict)

def _rand(self, args, ldict):
    ldict.last = args.newgroup(floatobj(random.random()))

def _ldict(self, args, ldict):
    ldict.last = args.newgroup(dictobj(ldict.deepcopy()))
    del ldict.last.base.base.last
def _itos(self, args, ldict):
    assert 0, args
_definedfuncs = {
    'rand':_rand,
    'ldict':_ldict,
    'itos':_itos
}