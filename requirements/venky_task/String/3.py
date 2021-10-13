def venky(s):
  if 2<len(s):
    print(s[:2]+s[-2:])
  else:
    return "empty string"
n=input("enter a stirng :")
venky(n)
