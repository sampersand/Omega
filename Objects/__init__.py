from Objects.Obj import obj
from Objects.NullObj import nullobj
from Objects.NumObj import numobj, boolobj, floatobj, intobj
from Objects.MthdObj import funcobj, operobj, ufuncobj
objregexes = {
    r'(?:0[bBoOxXdD])?\d+[nN]':intobj
    r'true|false':boolobj
}
__all__ = frozenset(['objregex']  + list(x for x in locals() if x[-3:] == 'obj'))
