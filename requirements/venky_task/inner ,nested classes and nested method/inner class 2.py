'''
class Person():
  def __init__(self):
    self.name="venky"
    self.dob=self.DOB()
  def display(self):
    print("name :",self.name)
    self.dob.display()

  class DOB():
    def __init__(self):
      self.data=14
      self.month="06"
      self.year=1995
    def display(self):
      print("DOB: {}/{}/{}".format(self.data,self.month,self.year))

p=Person()
p.display()


q=p.DOB()
q.display()

'''
class Person():
  def __init__(self):
    self.name="venky"
    self.dob=self.DOB()
  def display(self):
    print("name :",self.name)
    self.dob.display()

  class DOB():
    def __init__(self):
      self.data=14
      self.month="06"
      self.year=1995
    def display(self):
      print("DOB: {}/{}/{}".format(self.data,self.month,self.year))

p=Person()
p.display()


#q=Person.DOB()
#q.display()
