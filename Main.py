if __name__ == '__main__':
    if __debug__:
        assert 0
        print("@herelol")
    from File import file
    f = file('testcode.om')
    print(f)
    print('--')
    ldict = f.eval()
    print('--')
    if __debug__:
        print('LocalsDict ::', ldict)

