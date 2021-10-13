def cube(a,func):
  q=func(a)
  return a*q
def square(b):
  return b*b
p=cube(10,square)
print(p)
