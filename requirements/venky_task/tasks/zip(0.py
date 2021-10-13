numberList = [1, 2, 3]
strList = ['one', 'two', 'three']


result = zip()

resultList = dict(result)
print(resultList)

# Two iterables are passed
result = zip(strList,numberList)
print(result)
# Converting itertor to set
resultSet = dict(result)
print(resultSet)
