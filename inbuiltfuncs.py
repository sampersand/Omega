def evalfunc(base, eles, locls):
    pass
def evaloper(base, eles, locls):
    name = str(base)
    import control
    if __debug__:
        assert base is eles.base #shouldn't be any other way...
        assert name in control.allopers #how would it get passed here??
    if name in control.alldelims:
        if name in control.delims['endline'][0]:
            for ele in eles:
                ele.eval(locls) # _should_ set locls['$'] by itself
        elif name in control.delims['applier'][0]:
            assert 0, repr(eles)
        elif name in control.delims['arraysep'][0]:
            from group import group
            from obj import arrayobj
            ret = arrayobj()
            for ele in eles:
                ele.eval(locls)
                ret.base.append(locls['$'])
            locls['$'] = group(base = ret)
        else:
            raise SyntaxError("Special Operator '{}' isn't defined yet!".format(name))
    elif '<' == name[0] and name[-1] == '-' or name[0] == '-' and name[-1] == '>':
        """
            hm... take the following code:

                    a <- 4;
                    b <- 2;
                    1 + 2 -+> a -+> b 

            regardless of how '-+>' is percieved,

                    a == 7

            However, should:

                    b == 5 #(aka the '$' from 1 + 2 and b's old value)#

            or should:

                    b == 9 #(aka the '$' right before it's evaluated and b's old value)#

            I think i'll go wtih the second option.
        """
        d = name[0] == '-'
        name = name[1:-1]
        eles[1 - d].eval(locls)
        for ele in eles[slice(d or None, 1 - d or None, None)]:
            _ioperfunc(name, ele, locls)
    else:
        eles[0].eval(locls)
        for ele in eles[1:]:
            last = locls['$']
            ele.eval(locls)
            locls['$'].base.updatebase(name, last.base)

def _ioperfunc(sname, ele, locls): #sname == stripped name
    #DO NOT USE STR IN THE FUTURE. IT WILL MESS EVERYTHING UP!
    if sname == '':
        locls[str(ele)] = locls['$']
    else:
        if str(ele) not in locls:
            assert 0, 'what happens here??'
            locls[str(ele)] = locls['$']
            return
        else:
            import control
            from group import group
            g = group(base = control.allopers[sname], args = [locls[str(ele)], locls['$']])
            g.eval(locls)
            import copy
            locls[str(ele)] = copy.deepcopy(locls['$'])





















