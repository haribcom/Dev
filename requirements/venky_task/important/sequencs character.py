def venky(s):
  a={}
  for i in s:
    if i in a:
      a[i]+=1
    else:
      a[i]=1
  return a

n=input("enter a string:")
print(venky(n))
  
