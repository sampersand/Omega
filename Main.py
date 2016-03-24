if __name__ == '__main__':
    if __debug__:
        from time import clock #yes, i understand that clock is depreciated.
        start = clock()
    from File import file
    f = file('/Users/westerhack/code/python/Omega/omcode/linkedlist.om') #hardcode ftws
    # f = file('/Users/westerhack/code/python/Omega/omcode/gamesbackup.om') #hardcode ftws
    print(f)
    print('--')
    ldict = f.eval()
    print('--')
    if __debug__ and '$dnd' not in ldict:
        print('Locals Str ::', str(ldict),'\n')
        print('Locals Repr ::', repr(ldict),'\n')
        print('Total Elapsed Time ::', clock() - start, 'seconds\n')
 
