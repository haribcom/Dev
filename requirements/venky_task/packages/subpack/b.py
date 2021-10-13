class myaddress():
  def __init__(self,place,company):
    self.place=place
    self.company=company
  def disp(self):
    print("i am in {} and working in {}".format(self.place,self.company))
