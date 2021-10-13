def venky(s):
  a=dict()
  for i in s:
    if i in a:
      a[i]+=1
    else:
      a[i]=1
  print(a.value.sort())

n=input("enter a string: ")
venky(n)
      
