from numpy import *
n=array([[1,2,3],[4,5,6]])
n.shape=(6,1)
m=n.reshape(1,6)
print(m)

print()
a=arange(24)
a.shape=(6,4)
print(a)

b=array([1,2,3,4,5])
print(a.itemsize)

c=zeros(5)
print(c)
c=zeros(5,int)
print(c)
c=ones(5,int)
print(c)
c=ones((3,3),int)
print(c)


d=array([1,2,3,4,5,6.0])
print(d.size)
d=array([1,2,3,4,5,6])
print(d.dtype)


































