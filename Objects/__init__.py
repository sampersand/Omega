from Objects.Obj import obj
from Objects.NullObj import nullobj
from Objects.NumObj import numobj, boolobj, floatobj
from Objects.MthdObj import funcobj, operobj, ufuncobj
objregexes = {
    
}
__all__ = frozenset(['objregex']  + list(x for x in locals() if x[-3:] == 'obj'))
