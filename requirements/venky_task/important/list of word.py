
def venky(l):
  a=[]
  for i in l:
    a.append((len(i), i))
   
  a.sort()
  print(a)
  return a[-1][1]
print(venky(["venky","venkat","venkatesh","venn"]))
