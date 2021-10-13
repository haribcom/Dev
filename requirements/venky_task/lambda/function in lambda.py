def cube(a,func):
  p=func(a)
  return p*a
q=cube(10,lambda b:b*b)
print(q)
