a=10
def g():
  
  global a
  a=20
  print(a)
g()
print(a)




print()
b=30
c=200
print(id(b))
def gls():
  b=9
  x=globals()['b']
  print(id(x))
  print("fun in b",b)
  globals()['b']=300
  print("fun in b",b)
gls()
print("out in b",b)
print("out in c",c)
print(id(b))
  
