n=int(input("enter the number"))
a=0
b=1
while(n>1):
  c=a+b
  print(a)
  a=b
  b=c
  n=n-1


for i in range(n):
  print(a)
  t=a
  a=b
  b=t+a
