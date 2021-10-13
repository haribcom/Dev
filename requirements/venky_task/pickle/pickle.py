import pickle

class emp():
  def __init__(self,ename,eno,eaddr,role):
    self.ename=ename
    self.eno=eno
    self.eaddr=eaddr
    self.role=role
  def display(self):
    print(self.ename,"\t",self.eno,"\t",self.eaddr,"\t",self.role)
with open("venkyfun.txt","wb") as f:
  a=input("enter a ename: ")
  b=input("enter a eno: ")
  c=input("enter eaddr: ")
  d=input("enter a role: ")
  e=emp(a,b,c,d)
  pickle.dump(e,f)
  print("data is dump to ",repr("venkyfun.dat"),"file")


with open("venkyfun.txt","rb") as k:
  obj=pickle.load(k)
  print("dumped data shown here")
  obj.display()
  
