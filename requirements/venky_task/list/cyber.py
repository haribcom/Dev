l1=["a","b","c"]
l2=["a","b"]
c=[]
d=[]
for i in l1:
  if i in l2:
    c.append(i)
  else:
    d.append(i)
    print(c,d)
