n=int(input("enter the number: "))
b=1
for i in range(0,n):
  for j in range(0,i):
    print(end=" ")
  for k in range(0,n-i-1):
    print("*",end=" ")
   
  print()

input()
