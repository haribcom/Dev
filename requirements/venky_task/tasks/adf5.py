a=[2,7,5,9,6,8,10]
b=[a[0]]
n=0
for i in range(len(a)):
  if b[-1]<a[i]:
    b.append(a[i])
print(b)





"""n=n+1
  for j in range(n-1,n+1):
    if j>=len(a):
      break
    if a[i]<a[j]:
      b.append(a[j]) 
print(len(b))
print(b)
"""
