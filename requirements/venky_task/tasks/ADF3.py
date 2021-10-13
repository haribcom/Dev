a=[2,5,6,3,4,5,8,5,6,98,5,2,3]

for i in a:
  b=a.count(i)
  if b>1:
    for j in range(b):
      a.remove(i-1)
print(a)



