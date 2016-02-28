def evalfunc(base, eles, locls):
    name = str(base)
    if name == 'disp':
        from obj import strobj
        args, sep, end = ('', ), ', ', '\n'
        if len(eles) > 0:
            if __debug__:
                assert not eles[0].base.isnull(), 'when would it be?'
            if not eles[0].base.isnull():
                if not eles[0]:
                    eles[0].eval(locls)
                    args = (locls.lv.base.strobj.scrub(), )
                else:
                    def scrub(ele, locls):
                        print(repr(ele),repr(locls))
                        ele.eval(locls)
                        return locls.lv.base.strobj.scrub()
                    args = [scrub(ele, locls) for ele in eles[0]]
            if len(eles) > 1:
                if not eles[1].base.isnull():
                    if __debug__:
                        assert isinstance(eles[1].base, strobj)
                    sep = eles[1].base.scrub()
                if len(eles) > 2:
                    if not eles[2].base.isnull():
                        if __debug__:
                            assert isinstance(eles[2].base, strobj)
                        end = eles[2].base.scrub()
        print(*args, sep = sep, end = end)
    elif name == 'if':
        from group import group
        cond, iftrue, iffalse = locls.lv, group(), group()
        if len(eles) > 0:
            cond = eles[0]
            if len(eles) > 1:
                iftrue = eles[1]
                if len(eles) > 2:
                    iffalse = eles[2]
                    if __debug__:
                        if len(eles) > 3:
                            raise SyntaxError('Not allowed to have more than 3 arguments for if statement(s)!')
        cond.eval(locls)
        (iftrue if locls.lv.base else iffalse).eval(locls)
    elif name == 'skip':
        pass #keep this here.
    elif name == 'rm':
        if not eles:
            locls.clear()
        else:
            if __debug__:
                assert len(eles) == 1, "only 1 thing after the semicolon..."
            if not eles[0]:
                del locls[str(eles[0])]
            else:
                for ele in eles[0]:
                    del locls[str(ele)]
        if '$' not in locls:
            from group import group
            locls.lv = group()
    elif name == 'for':
        if __debug__:
            assert len(eles) == 2, 'for:(init;cond;inc):(statement(s))'
            assert len(eles[0]) == 3, 'for:(init;cond;inc):(statement(s))'
        eles[0][0].eval(locls) #initialization
        while True:
            eles[0][1].eval(locls) #evaluate the condition
            if not locls.lv.base:
                break
            eles[1].eval(locls) #execute the statement(s)
            eles[0][2].eval(locls) #increment
    elif name == 'abort':
        if __debug__:
            assert len(eles) <= 1, 'abort[:message]'
        if len(eles) == 1: #abort w/ message
            eles[0].eval(locls)
        else:
            from group import group
            from obj import nullobj
            locls.lv = group(base = nullobj())
        quit('Aborting!' + (str(locls.lv) and " Message: " + str(locls.lv)))
    elif name == 'whilst':
        if __debug__:
            assert len(eles) == 2, 'whilst:(cond):(statement(s))'
        while True:
            eles[0].eval(locls) #evaluate the condition
            if not locls.lv.base:
                break
            eles[1].eval(locls) #execute the statement(s)
    elif name == 'func':
        eles[0].eval(locls)
        name = str(locls.lv)
        args = eles[1]
        func = eles[2]
        from group import group
        from obj import usermethodobj
        locls[name] = group(base = usermethodobj(name, args, func))
        locls.lv = locls[name]
    elif name == 'return':
        eles[0].eval(locls)
        locls.ret = locls.lv
    elif name == 'om':
        evalconsts(base, eles, locls)
    else:
        raise SyntaxError("Unknown function '{}'!".format(name))
def evaloper(base, eles, locls):
    name = str(base)
    import control
    if __debug__:
        assert base is eles.base #shouldn't be any other way...
        assert name in control.allopers #how would it get passed here??
    if name in control.alldelims:
        if name in control.delims['endline'][0]:
            for ele in eles:
                ele.eval(locls) # _should_ set locls.lv by itself
                if not locls.ret.base.isnull():
                    return
        elif name in control.delims['applier'][0]:
            if str(eles[0]) not in locls:
                eles[0].eval(locls)
            else:
                locls.lv = locls[str(eles[0])]
            locls.lv.base.eval(eles[1:], locls)
        elif name in control.delims['arraysep'][0]:
            from group import group
            from obj import arrayobj
            ret = arrayobj()
            for ele in eles:
                ele.eval(locls)
                ret.base.append(locls.lv)
            locls.lv = group(base = ret)
        else:
            raise SyntaxError("Special Operator '{}' isn't defined yet!".format(name))
    elif name in control.opers['binary']['assignment']: #aka assignment
        d = name[0] == '-'
        name = name[1:-1]
        eles[1 - d].eval(locls)
        for ele in eles[slice(d or None, 1 - d or None, None)]:
            _ioperfunc(name, ele, locls)
    elif name in control.opers['binary']['logic']:
        eles[0].eval(locls)
        for ele in eles[1:]:
            last = locls.lv
            ele.eval(locls)
            locls.lv = last.base.comparebase(last, name, locls.lv)
    elif name in control.opers['unary']['l'] or name in control.opers['unary']['r']:
        evalunary(base, eles, locls)
    else:
        eles[0].eval(locls)
        import control
        for ele in eles[1:]:
            last = locls.lv
            ele.eval(locls)
            locls.lv.base.updatebase(name, last.base)
def _ioperfunc(sname, ele, locls): #sname == stripped name
    """

        !!! DO NOT USE STR IN THE FUTURE. IT WILL MESS EVERYTHING UP !!!

        aka, remove locls[str(eles)]


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
    import obj
    last = locls.lv
    # ele.eval(locls)]
    # elestr = str(locls.lv)
    elestr = str(ele)
    if sname == '':
        locls[elestr] = last
        import copy
        locls.lv = copy.deepcopy(locls[elestr])
        # quit()
    else:
        if elestr not in locls:
            locls[elestr] = last
            #assert 0, 'what happens here?? '+elestr+'\n\n' + str(ele) + '\n\n' + str(locls)+'\n\n'+repr(last)
            return
        else:
            import control
            from group import group
            group(base = control.allopers[sname], args = [last, locls[elestr]]).eval(locls)
            import copy
            locls[elestr] = copy.deepcopy(locls.lv)


def evalunary(base, eles, locls):
    name = str(base)
    import control
    if __debug__:
        assert base is eles.base #not necessary, just figured.
        if name in control.opers['unary']['l']:
            assert eles[0].base.isnull(), eles #unary l should have null on the left (~X has no left term)
        else:
            assert len(eles) == 1
    if name == '>+' or name == '>-':
        from group import group
        from obj import intobj
        group(base = control.allopers['-%s>'%name[1]], args = [ group(base = intobj(1)), eles[1]]).eval(locls)
    elif name == '+<' or name == '-<':
        from group import group
        from obj import intobj
        import copy;
        eles[0].eval(locls)
        # ret = copy.deepcopy(locls[str(eles[0])]);
        ret = copy.deepcopy(locls.lv);
        group(base = control.allopers['-%s>'%name[0]], args = [ group(base = intobj(1)), eles[0]]).eval(locls)
        locls.lv = ret
    elif name == '!':
        import math
        eles[0].eval(locls)
        locls.lv.base.base = math.factorial(locls.lv.base.base)
    elif name == 'pos' or name == 'neg':
        eles[1].eval(locls)
        locls.lv.base.base = locls.lv.base.base
    elif name == 'b~':
        eles[1].eval(locls)
        locls.lv.base.base = ~locls.lv.base.base
    else:
        raise SyntaxError("Unknown unary function '{}'!".format(name))
def evalconsts(base, eles, locls):
    name = str(base)
    if name == 'om':
        fname = str(eles[0])
        if fname == 'locls':
            from group import group
            from obj import dictobj
            locls.lv = group(base = dictobj(locls))
        elif fname == 'rand':
            import random
            from group import group
            from obj import floatobj
            locls.lv = group(base = floatobj(random.random()))
        else:
            raise SyntaxError("Unknown om function '{}'!".format(fname))
    else:
        raise SyntaxError("Unknown const function '{}'!".format(name))
def evalarray(base, eles, locls):
    if __debug__:
        assert len(eles) > 0, 'cant pass no arguments to an array!'
    name = str(eles[0])
    if name == 'len':
        locls.lv = base.lengrp
    elif name == 'get':
        if __debug__:
            assert len(eles) == 2, 'array:get:pos not %s' % repr(eles)
        eles[1].eval(locls)
        locls.lv = base.base[locls.lv.base.base]
    elif name == 'set':
        if __debug__:
            assert len(eles) == 2, 'array:set:pos,toset :: not '+str(len(eles))
            assert len(eles[1]) == 2, 'array:set:pos,toset :: not '+str(len(eles[1]))
        eles[1][0].eval(locls) #eval pos
        pos = locls.lv.base.base #set pos to locls.lv
        eles[1][1].eval(locls) #evaluate toset
        base.base[pos] = locls.lv.base.base #set ele @ pos to locls.lv
    elif name == 'add':
        if __debug__:
            assert len(eles) == 2, 'array:add:[pos,]element'
            assert len(eles[1]) == 0 or len(eles[1]) == 2, 'array:add:[pos,]element (not %s)'%len(eles[1])
        import control
        if len(eles[1]) == 0 or eles[1].basestr not in control.delims['arraysep'][0]:
            eles[1].eval(locls)
            base.base.append(locls.lv)
        else:
            eles[1][0].eval(locls)
            pos = locls.lv.base.base
            eles[1][1].eval(locls)
            base.base.insert(pos, locls.lv)
    elif name == 'rem':
        if __debug__:
            assert len(eles) == 1 or len(eles) == 2, 'array:rem:[pos]'
        if len(eles[1]) == 0:
            del base.base[-1]
        else:
            eles[1].eval(locls)
            del base.base[locls.lv.base.base]
    elif name == 'pop':
        if __debug__:
            assert len(eles) == 2, 'array:pop:[pos]'
        if len(eles[1]) == 0:
            locls.lv = base.base.pop(-1)
        else:
            eles[1].eval(locls)
            locls.lv = base.base.pop(locls.lv.base.base)
    elif name == 'copy':
        if __debug__:
            assert len(eles) == 2, 'array:copy:()'
        from group import group
        import copy
        locls.lv = group(base=copy.copy(base))
    else:
        raise SyntaxError("Unknown array function '{}'!".format(name))
    


















