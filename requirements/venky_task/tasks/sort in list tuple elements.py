a=[(1,2),(5,2),(2,8),(2,1),(5,5),(2,5)]

def last(last):
  return last[-1]
def list(a):
  
  return sorted(a,key=last)

print(list(a))
