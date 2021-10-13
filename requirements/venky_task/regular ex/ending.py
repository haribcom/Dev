import re
a="venky is a python developer venky"
b=re.search("$venky",a)
if b!=None:
  print("is ends with ",b.group())
else:
  print("not ends with...",b)


"""n=input("enter a string : ")
a=re.match(r"[a-k][0369][a-zA-Z0-9]*",n)
if a!=None:
  print("the string is matched....")
else:
  print("Not matched....")"""
