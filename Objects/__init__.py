import re
floatre = re.compile(r'^(\d*\.?\d+)(?:[eE]([nNpP]?)(\d+))?F?$') #float can have fF at the end
decre = re.compile(r'^(?:0([dD]))?(\d+)I?$')    #can have 'I' at the end
binre = re.compile(r'^0([bB])([01]+)I?$')       #can have 'I' at the end
hexre = re.compile(r'^0([xX])([\dA-Fa-f]+)I?$') #can have 'I' at the end
octre = re.compile(r'^0([oO])([0-7]+)I?$')      #can have 'I' at the end
unire = re.compile(r'^0[uU](\d+)[uU](\d+)I?$')  #can have 'I' at the end
nbases = {'d':10, '':10, 'b':2, 'x':16, 'o':8}

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