from Objects import Obj
obj = Obj.obj

from Objects import NullObj, MethodObj
methodobj = MethodObj.methodobj
nullobj = NullObj.nullobj

from Objects import StrObj, NumObj
strobj = StrObj.strobj
numobj = NumObj.numobj

from Objects import IntObj, FloatObj
intobj = IntObj.intobj
floatobj = FloatObj.floatobj

from Objects import BoolObj
boolobj = BoolObj.boolobj

from Objects import DictObj, ArrayObj
dictobj = DictObj.dictobj
arrayobj = ArrayObj.arrayobj

from Objects import FuncObj, OperObj
funcobj = FuncObj.funcobj
operobj = OperObj.operobj

from Objects import UserFuncObj
userfuncobj = UserFuncObj.userfuncobj

__all__  = [x for x in locals().keys() if x[-3:] == 'obj']
