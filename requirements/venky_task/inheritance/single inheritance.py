class one():
  def m1(self):
    print("it m1 of one")

class two(one):
  def m2(self):
    print("it m2 of")
t=two()
print(t.__hash__())
t.m2()
t.m1()

print()
class a():
  def m3(self):
    print("this is a child class ")
r=a()
r.m3()
p=r.__hash__()
print(r.__str__())
print(a.__bases__)
print(p)
