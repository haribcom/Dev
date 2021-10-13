def venky(s):
  for i in s.split("\n"):
    print("".join(i.split()[::-1]))
  print(" ".join(s.split()[::-1]))

n=input("enter astring :")
venky(n)
