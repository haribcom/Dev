n=int(input("enter a number: "))

if n>1:
  for i in range(2,n):
    if n%i==0:
      print(n,"not a prime number:")
      break
  else:
    print("its prime number")
