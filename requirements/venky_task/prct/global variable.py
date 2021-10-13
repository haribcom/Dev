a=10
def gl():
  a=20
  print("in function",a)
gl()
print("out function",a)



print()
b=100
def ab():
  print("in function",b)
ab()
print("out function",b)



print()
c=200
def ac():
  global c
  c=300
  print("in function",c)
ac()
print("out function",c)




print()
d=400
def ad():
  global d
  d=500
  print("in dunction",d)
def ad1():
  print("second funnction",d)
ad()
ad1()












