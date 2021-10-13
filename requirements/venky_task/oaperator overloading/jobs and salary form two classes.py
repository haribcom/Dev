class salarysheet:
  def __init__(self,name,salary):
    self.name=name
    self.salary=salary
  def __mul__(self,other):
    b=self.salary*other.days
    return b
  

class daysheet:
  def __init__(self,name,days):
    self.name=name
    self.days=days
  def __mul__(self,other):
    a=self.days*other.salary
    return a

s=salarysheet("venky",54000)
d=daysheet("venky",12)
print("the annual package is :",d*s)# This is daysheet class 
print("The packege is :",s*d)# this is for salarysheet














91
