class a:
  def __init__(self,a=None,b=None,c=None):
    print("This is a consturcto overloading")
t1=a()
t2=a(10)
t1=a(10,20,30)
print()

print("class b")
class b:
  def __init__(self,*a):
    print("This is a class b consturcto overloading")
t1=b()
t2=b(10)
t1=b(10,20,30)

