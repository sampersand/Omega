def evalfunc(base, eles, locls):
    pass
def evaloper(base, eles, locls):
    name = str(base)
    import control
    if __debug__:
        assert base is eles.base #shouldn't be any other way...
        assert name in control.allopers #how would it get passed here??
    if name in control.alldelims:
        if name in control.delims['arraysep'][0]:
            from group import group
            from obj import arrayobj
            ret = arrayobj()
            for ele in eles:
                ele.eval(locls)
                ret.base.append(locls['$'])
            locls['$'] = group(base = ret)
        elif name in control.delims['endline'][0]:
            for ele in eles:
                ele.eval(locls) # _should_ set locls['$'] by itself
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
        if name[0] == '-':
            eles[0].eval(locls)
            for ele in eles[1:]:
                _ioperfunc(name[1:-1], ele, locls)
        else:
            assert 0, 'not ready for backwards arrows yet'
    else:
        eles[0].eval(locls)
        for ele in eles[1:]:
            _operfunc(name, ele, locls)
def _operfunc(name, ele, locls):
    if __debug__:
        assert str(ele) in locls
    if name == '+':
        locls['$'] =
def _ioperfunc(sname, ele, locls): #sname == stripped name
    #assuming the direction is '->'
    if sname == '':
        #DO NOT USE STR IN THE FUTURE. IT WILL MESS EVERYTHING UP!
        locls[str(ele)] = locls['$']
        locls['$'] = locls[str(ele)]
    else:
        if str(ele) not in locls:
            locls[str(ele)] = locls['$']
            locls['$'] = locls[str(ele)]
            return
        else:
            import control
            from group import group
            group(base = control.allopers[sname], args = [locls[str(ele)], locls['$']]).eval(locls)
            locls[str(ele)] = locls['$']
            locls['$'] = locls[str(ele)]





















