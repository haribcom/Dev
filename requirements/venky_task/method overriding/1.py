class a:
  def name(self):
    print("My name venky")
  def course(self):
    print("Python")
class b(a):
  def course(self):
    print("My job is python developer")
    super().course()
t1=b()
t1.course()
t1.name()


