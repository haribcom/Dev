def venky(a,l):
  b=[]
  for i in l.split():
    if len(i)>a:
      b.append(i)
  return b
print(venky(2,"venky is a python developer"))
