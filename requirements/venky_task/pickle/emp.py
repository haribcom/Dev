class employee():
  def __init__(self,ename,eno,eaddr,role):
    self.ename=ename
    self.eno=eno
    self.eaddr=eaddr
    self.role=role
  def display(self):
    print(self.ename,"\t",self.eno,"\t",self.eaddr,"\t",self.role)
