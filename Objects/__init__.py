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
from Objects.StrObj import strobj
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

#####
# Collection Objects
#
from Objects.CollectionObjects.CollectionObj import collectionobj

from Objects.CollectionObjects.ArrayObj import arrayobj
from Objects.CollectionObjects.DictObj import dictobj
#
#
#####

objregexes = {
    r'(?:0[bBoOxXdD])?\d+[nN]?' : intobj,
    r'[tT]rue|[fF]alse' : boolobj,
    r'[nN](?:ull|il|one)' : nullobj,
    r'\d*(\.)?\d+([eE][nNpP]?\d+)?(?(1)[fF]?|[fF])' : floatobj,
    r'\d*\.?\d+([eE][nNpP]?\d+)?[iIjJ]' : complexobj,
    r'(?P<quote>[{quote}]).*(?!\{escape})(?P=quote)' : strobj
}

__all__ = frozenset(['objregex']  + list(x for x in locals() if x[-3:] == 'obj'))









