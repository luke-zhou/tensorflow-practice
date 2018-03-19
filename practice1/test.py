test_array =[
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

print(test_array)

square_array = [[y*y for y in x] for x in test_array]

print (square_array)