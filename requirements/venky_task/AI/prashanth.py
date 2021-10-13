a=[0,0,1]
b=[1,0,0]
c=[]
for i in range(len(a)):
  if a[i]!=b[i]:
    c.append(0)
  else:
    c.append(1)
print(c)
