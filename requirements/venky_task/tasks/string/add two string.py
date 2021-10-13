a="abc"
b="xyz"
c="123"
i=0
j=0
k=0
o=""
while i<len(a) or j<len(b) or k<len(c):
  o=o+a[i]+b[j]+c[k]
  i=i+1
  j=j+1
  k+=1
print(o)
