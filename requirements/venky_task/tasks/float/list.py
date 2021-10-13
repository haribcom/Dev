a=[1,2,3,5,7,8,10]
a.sort()
print(a)
b=[]
for i in range(a[0],a[-1]):
  if i not in a:
    b.append(i)
print(b)
