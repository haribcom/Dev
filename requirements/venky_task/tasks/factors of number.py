def fact(n):
  print("The factor of ",n,"are")
  for i in range(1,n+1):
    if n%i==0:
      print(i)
fact(8)
