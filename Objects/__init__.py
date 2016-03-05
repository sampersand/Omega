#####
# Object Class
#
from Objects.Obj import obj
#
#
#####


#####
# Misc Objects
#
from Objects.NullObj import nullobj
#
#
#####


#####
# Number Objects
#
from Objects.NumberObjects.NumObj import numobj

from Objects.NumberObjects.IntObj import intobj
from Objects.NumberObjects.FloatObj import floatobj

from Objects.NumberObjects.BoolObj import boolobj
from Objects.NumberObjects.ComplexObj import complexobj
#
#
#####


#####
# Method Objects
#
from Objects.MethodObjects.MthdObj import mthdobj

from Objects.MethodObjects.OperObj import operobj
from Objects.MethodObjects.FuncObj import funcobj

from Objects.MethodObjects.UFuncObj import ufuncobj
#
#
#####

import re

objregexes = {
    re.compile(r'(?:0[bBoOxXdD])?\d+[nN]?'):intobj,
    re.compile(r'[tT]rue|[fF]alse'):boolobj,
    re.compile(r'[nN](?:ull|il|one)'):nullobj,
    re.compile(r'\d*(\.)?\d+([eE][nNpP]?\d+)?(?(1)[fF]?|[fF])'):floatobj,
    re.compile(r'\d*\.?\d+([eE][nNpP]?\d+)?[iIjJ]'):complexobj,
}

__all__ = frozenset(['objregex']  + list(x for x in locals() if x[-3:] == 'obj'))
