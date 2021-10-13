"""class Employee:
  def __init__(self,ename,eno,esal):
    self.ename=ename
    self.eno=eno
    self.esal=esal
  def display(self):
    print("Employee name: ",self.ename)
    print("Employee no: ",self.eno)
    print("Employee esal: ",self.esal)

class Test():
  def modify(emp):
    emp.esal=emp.esal+10000
    emp.display()


a=Employee("venky",1236,60000)
Test.modify(a)"""


class Employee():
  def __init__(self,name,no,sal):
    self.name=name
    self.no=no
    self.sal=sal
  def display(self):
    print("Name :",self.name)
    print("No :",self.no)
    print("Sal :",self.sal)

class Test():
  def modify(m):
    m.sal=m.sal+10000
    m.display()
a=Employee("venky",1236,50000)
Test.modify(a)





    



  

