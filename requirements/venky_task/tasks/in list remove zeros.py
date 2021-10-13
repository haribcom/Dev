a=[1,1001,100101,10010100,2,202,20022,22]
b=[]
for i in a:
  s=""
  for j in str(i):
    if int(j)!=0:
      s=s+j
  b.append(int(s))
print(b)

print()
for k in a:
  k.remove(0)
print(a)
