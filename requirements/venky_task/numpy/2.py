import numpy as np

a=np.array([[1,2,3],[4,5,6]])
print(a)
print(a[1][1])

print()
a.shape=(2,3)
a.shape=(3,2)
print(a)

b=np.array([[1,2,3],[4,5,6]])
b=b.reshape(3,2)
print(b)

arr=np.arange(24)
arr2=arr.reshape(6,4)
print(arr2)


c=np.array([1,2,5,3,6])
print(c.itemsize)

d=np.ones((3,2),int)
print(d)
