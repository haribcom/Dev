a=[1,2,5,-5,-2,5,6,8,-22222]
"""for i in range(len(a)):
  for j in range(len(a)):
    if a[i]<a[j]:
      t=a[i]
      a[i]=a[j]
      a[j]=t
print(a)
print("the least :",a[0]," max values: ",a[-1])"""

l=a[0]
m=a[0]
for i in a:
  if i<l:
    l=i
  elif i>m:
    m=i
print("least : ",l,"\n max : ",m)


