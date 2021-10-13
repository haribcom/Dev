def venky(s):
  for i in s:
    if s[0]==i:
      print(s[0]+s[1:].replace(i,"@"))
    else:
      pass
n=input("enter a stirng  :")

venky(n)
