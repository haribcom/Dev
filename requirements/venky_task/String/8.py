def venky(l,n):
  p=l[:n]
  q=l[n+1:]
  return p+q

n=input("enter a string :")
s=int(input("enter a num :"))
print(venky(n,s))
