
def venky(l):
  a=[]
  for i in l:
    a.append((len(i), i))
  a.sort()
  return a[-1][1]
print(venky(["venky","venkat","venkatesh","venn"]))
