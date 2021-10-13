a=(1,"venkat",10.25)
a,b,c=a
print(a,type(a))
print(b,type(b))
print(c,type(c))
print()

a,b,c,d=1,"venkat",{"a":1236},[1,[2,3,4]]
print(a,type(a))
print(b,type(b))
print(c,type(c))
print(d,d[1][2])

e=[1,[2,3,4]]
print(e[1][1])

f=[10,20,]
print(f,type(f))
