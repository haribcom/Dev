x=[0,1,2,3]
for x[1] in x:
  print(x[1])



a=[1,2,3,5,4,1,2,53]
for i in range(len(a)):
  for j in range(len(a)):
    if a[i]<a[j]:
      t=a[i]
      a[i]=a[j]
      a[j]=t
print(a)
      
