import sys
sys.path.append('../src')
import preprocess

def test_nGroup():
    testList =[1,2,3,None,5,6,7,8,9]
    for r in preprocess.nGroup(testList, 3):
        print(r)

def test_isGroupVaild():
    testList1 =[
        ['1999-01-24',22.577700,22.577700,22.378700,22.537901,22.537901,691858],
        ['1999-01-25','null','null','null','null','null','null'],
        ['1999-01-26',22.965599,22.965599,22.726900,22.915800,22.915800,1463623],
        ['1999-01-27',23.472799,23.472799,22.876101,23.423100,23.423100,1572709]
        ]
    print(preprocess.isGroupValid(testList1))
    testList2 =[
        ['1999-01-24',22.577700,22.577700,22.378700,22.537901,22.537901,691858],
        ['1999-01-25','null','null','null','null','null','null'],
        ['1999-01-26',22.965599,22.965599,22.726900,22.915800,22.915800,1463623],
        ['1999-01-27','null','null','null','null','null','null']
        ]
    print(preprocess.isGroupValid(testList2))
    testList3 =[
        ['1999-01-24','null','null','null','null','null','null'],
        ['1999-01-25','null','null','null','null','null','null'],
        ['1999-01-26','null','null','null','null','null','null'],
        ['1999-01-27','null','null','null','null','null','null']
        ]
    print(preprocess.isGroupValid(testList3))
    testList4 =[
        ['1999-01-24',22.577700,22.577700,22.378700,22.537901,22.537901,691858],
        ['1999-01-25',22.965599,22.965599,22.726900,22.915800,22.915800,1463623],
        ['1999-01-26',22.965599,22.965599,22.726900,22.915800,22.915800,1463623],
        ['1999-01-27',23.472799,23.472799,22.876101,23.423100,23.423100,1572709]
        ]
    print(preprocess.isGroupValid(testList4))
    testList5 =[
        ['1999-01-24',22.577700,22.577700,22.378700,22.537901,22.537901,691858],
        ['1999-01-25',22.965599,22.965599,22.726900,22.915800,22.915800,1463623],
        ['1999-01-26',22.965599,22.965599,'null',22.915800,22.915800,1463623],
        ['1999-01-27',23.472799,23.472799,22.876101,23.423100,23.423100,1572709]
        ]
    print(preprocess.isGroupValid(testList5))

def test():
    testList =[ [1,2,3,4,5,6], 
                [2,3,4,5,6,7],
                [3,4,5,6,7,8], 
                [8,9,10,11,12,13],
                [9,10,11,12,13,14], 
                [10,11,12,13,14,15]
    ]
    result = preprocess.generate_features(testList)
    print(result)

if __name__=='__main__':
    test()
    print(0=='0')