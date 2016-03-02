if __name__ == '__main__':
    if __debug__:
        from time import clock #yes, i understand that clock is depreciated.
        start = clock()
    from File import file
    f = file('/Users/westerhack/code/python/Omega/testcode.om') #hardcode ftw
    print(f)
    print('--')
    ldict = f.eval()
    print('--')
    if __debug__ and '$dnd' not in ldict:
        print('LocalsDict ::', str(ldict))
        print('Total Elapsed Time ::', clock() - start, 'seconds')
 
