import copy

a=[1,2,3,[4,5]]
b=a.copy()
a[3][1]=10
print(b)
print(a)

print()
x=[7,8,[4,5]]
y=copy.deepcopy(x)
x[2][1]=50
print(y)
print(x)
