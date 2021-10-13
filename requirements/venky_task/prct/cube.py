def cube(n):
  n=n-1
  total=0
  while n>0:
    total=total+n*n*n
    n=n-1
  return total


print(cube(3))
