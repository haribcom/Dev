class a:
  def m1(self):
    print("in m1 of a")
  def m2(self):
    print("in m2 of a")
  def __str__(self):
    
    return "venky"
a1=a()
print(a1)
p=a1.__str__()
print(p)
a2=a()
print(a2)


print()

class b():
  def __init__(self,name):
    self.name=name
  def m1(self):
    print("in m1 of b")
  def __str__(self):
    return self.name
    
b1=b("venky of class B")
print(b1.__str__())
print(b1)
b1=b("venkyyyy")
print(b1)







