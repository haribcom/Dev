a=[1,2,5,6,3,1,4,7]
b=set(map(lambda s:s+2 ,a))
print(b)

d={1:"python"}
s=d.values()
print(s)
print(d[1])


e=[4,635,-5,45]
a,b,c,d=e
big=a if a>b and a>c and a>d else (b if b>c and b>d else(c if c>d else d))
print(big)


l=e[0]
l1=e[0]
for i in e:
  if i>l:
    l=i
  if i<l1:
    l1=i
    
print(l)
print(l1)


