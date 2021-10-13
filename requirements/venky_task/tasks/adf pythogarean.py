a=[3,1,5,6,4]
n=1
for i in range(len(a)):
 
  for j in range(n,len(a)):
   
    for k in range(n+1,len(a)):
      if a[i]**2+a[j]**2==a[k]**2:
        print("True")
        print(a[i],a[j],a[k])
        break
  n=n+1
