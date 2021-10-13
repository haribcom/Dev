from functools import reduce
a=[1,2,5,3,6,8,9,4,1,0,20,28,56,99]
x=list(filter(lambda n:n%2==0,a))

y=list(map(lambda m:m*2,x))
z=str(reduce(lambda p,o:p+o,y))
print(a)
print("even numbers: ",x)
print("multiple with 2: ",y)
print("totol of these nubmers: ",z)

