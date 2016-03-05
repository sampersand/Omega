import re
from Objects.Obj import obj
from Objects.NullObj import nullobj
from Objects.NumObj import numobj, boolobj, floatobj, intobj, complexobj
from Objects.MthdObj import funcobj, operobj, ufuncobj
objregexes = {
    re.compile(r'(?:0[bBoOxXdD])?\d+[nN]?'):intobj,
    re.compile(r'[tT]rue|[fF]alse'):boolobj,
    re.compile(r'[nN](?:ull|il|one)'):nullobj,
    re.compile(r'\d*(\.)?\d+([eE][nNpP]?\d+)?(?(1)[fF]?|[fF])'):floatobj,
    re.compile(r'\d*\.?\d+([eE][nNpP]?\d+)?[iIjJ]'):complexobj,
}
__all__ = frozenset(['objregex']  + list(x for x in locals() if x[-3:] == 'obj'))
