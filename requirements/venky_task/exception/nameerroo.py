
try:
  a=eval(input("enter a"))
  b=eval(input("enter b"))

  c=a/b
  print(c)
except(NameError):
  print("enter only numbers")
except:
  print("other")
