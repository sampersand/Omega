if __name__ == '__main__':
    from File import file
    f = file('/Users/westerhack/code/python/Omega/testcode.om') #hardcode ftw
    print(f)
    print('--')
    ldict = f.eval()
    print('--')
    if __debug__ and '$dnd' not in ldict:
        print('LocalsDict ::', ldict)