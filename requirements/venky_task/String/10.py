def venky(n):
  b=[]
  a=n[0]+n[-1]
  b.append(a)
  print(b+n[1:-1])

print(venky(["venky","venkat","venky"]))
