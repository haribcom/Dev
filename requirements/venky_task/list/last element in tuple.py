def last(n):
  return n[-1]
def venky(lst):
  print(sorted(lst,key=last))
  

venky([(1,5),(2,1),(8,6),(4,2),(2,3)])

