a=[100,200,300,40,50,60,80,90]
b=a[0]
c=0
for i in a:
  if i<b:
    b=i
for j in a:
  if j>c:
    c=j
print(b)
print(c)
