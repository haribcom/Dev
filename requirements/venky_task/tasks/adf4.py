a=[1,2,3,4,5]
d={}
for i in a:
  d[i]=i*i
print(d)

c={i:i*i for i in a}
print(c)

