objregexes = {}
#####
# Level 0
#
from Objects.Obj import obj
#
#
#####

#####
# Level 1
#
from Objects.NullObj import nullobj
objregexes[r'[nN](?:ull|il|one)'] = nullobj

from Objects.TypeObj import typeobj
from Objects.StrObj import strobj
objregexes[r'[rR@]?(?P<quote>[{quote}])(?P<keep>.*)(?!\{escape})(?P=quote)'] = strobj

from Objects.NumberObjects.NumObj import numobj

from Objects.CollectionObjects.CollectionObj import collectionobj
from Objects.MethodObjects.MthdObj import mthdobj

from Objects.NumberObjects.IntObj import intobj
objregexes[r'(?:0[dD])?(?P<keep>(?:0[bBoOxXdD])?\d+)[nN]?'] = intobj

from Objects.NumberObjects.FloatObj import floatobj
objregexes[r'(?P<keep>\d*(?P<period>\.)?\d+(?:[eE][nNpP]?\d+)?)(?(period)[fF]?|[fF])'] = floatobj
# objregexes[r'(\d*(\.)?\d+([eE][nNpP]?\d+)?)(?(2)[fF]?|[fF])'] = floatobj

from Objects.NumberObjects.BoolObj import boolobj
objregexes[r'(?P<keep>[tT]rue|[fF]alse)'] = boolobj

from Objects.NumberObjects.ComplexObj import complexobj
objregexes[r'(?P<keep>\d*(?P<period>\.)?\d+(?:[eE][nNpP]?\d+)?[iIjJ])'] = floatobj


from Objects.CollectionObjects.ArrayObj import arrayobj
from Objects.CollectionObjects.DictObj import dictobj
from Objects.MethodObjects.OperObj import operobj

from Objects.MethodObjects.UMthdObj import umthdobj
from Objects.CollectionObjects.UClassObj import uclassobj

from Objects.MethodObjects.FuncObj import funcobj
from Objects.MethodObjects.OmFuncObj import omfuncobj

__all__ = frozenset(['objregex']  + list(x for x in locals() if x[-3:] == 'obj'))









