class Name:
  def __init__(self,name):
    self.name=name
    c=input("enter course :")
    self.job=self.JOB(c)
  def display(self):
    print("Name :",self.name)
    self.job.display()

  class JOB:
    def __init__(self,course):
      self.course=course
    def display(self):
      print("Designation :",self.course+" Developer")

s=input("enter a name: ")
n1=Name(s)
n1.display()

n1.job.display()
