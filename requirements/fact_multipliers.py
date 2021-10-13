'''
Given an array of integers, return a new array such that
each element at index i of the new array is the product of all the numbers
in the original array except the one i.
ex: inp = [1, 2, 3, 4, 5] then
    out = [120, 60, 40, 30, 24]
'''

from functools import reduce
l = [1,2,3,4,5]
fac = reduce(lambda x, y: x*y, l)
res = []
for i in l:
    if fac%i == 0:
            res.append(fac//i)
print(res)
