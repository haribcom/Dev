class a:
  def m1(self):
    print("this is m1 of a")
class b(a):
  def m2(self):
    print("this is a m2 of b")
class c(b):
  def m3(self):
    print("this is a m3 of c")
class d(c):
  def m4(self):
    print("this is a m4 of d")

r=d()
r.m1()
r.m2()
r.m3()
r.m4()
print()
p=d.__bases__
print(p)
