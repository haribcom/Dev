n=input("enter ur numbers: ")



while len(str(n))!=1:
  c=0
  for i in str(n):
    c+=int(i)
    n=c
  
print(n)

  
  
