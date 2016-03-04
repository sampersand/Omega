import re
floatre = re.compile(r'^(\d*\.?\d+)(?:[eE]([nNpP]?)(\d+))?[fF]?$') #float can have one of [fF] at the end
complre = re.compile(r'^(\d*\.?\d+)(?:[eE]([nNpP]?)(\d+))?[iIjJ]$') #compl needs to have one of [iIjJ] the end
intre = re.compile(r'^(0([xbodXBOD]|[uU]\d+[uU]))?[\dA-Fa-f]+$')
decre = re.compile(r'^(?:0([dD]))?(\d+)[dD]?$')    #can have one of '[dD]' at the end (digit)
binre = re.compile(r'^0([bB])([01]+)[dD]?$')       #can have one of '[dD]' at the end (digit)
hexre = re.compile(r'^0([xX])([\dA-Fa-f]+)[dD]?$') #can have one of '[dD]' at the end (digit)
octre = re.compile(r'^0([oO])([0-7]+)[dD]?$')      #can have one of '[dD]' at the end (digit)
unire = re.compile(r'^0[uU](\d+)[uU](\d+)[dD]?$')  #can have one of '[dD]' at the end (digit)
nbases = {'d':10, '':10, 'b':2, 'x':16, 'o':8}

from Objects.Object import ObjTypes
locals().update(ObjTypes._alldict)
__all__ = [x for x in locals().keys() if x[-3:] == 'obj']
