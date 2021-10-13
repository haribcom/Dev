class Error(Exception):
  pass
class ValueTooSmall(Error):
  pass
class ValueTooLarge(Error):
  pass



try:
  n=eval(input("enter a number: "))
  number=10
  if n<number:
    raise ValueTooSmall
  elif n>number:
    raise ValueTooLarge
  else:
    print("Perfect Matched")
except ValueTooLarge:
  print("The value is too large")
except ValueTooSmall:
  print("The value is too small")
except(NameError):
  print("Plese enter aonly numbers")
except:
  print("unexepected Error")
    
