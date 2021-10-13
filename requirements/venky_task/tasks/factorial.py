n=int(input("enter number: "))
a=1
for i in range(1,n+1):
  a=a*i
  print(a)

def fact(n):
  if n<1:
    return 1
  else:
    return (n*fact(n-1))

m=int(input("enter range: "))
print("the factorial of given number is",fact(m))
