class venky():
  def __init__(self,pages):
    self.pages=pages
  def __add__(self,other):
    t1=self.pages+other.pages
    return t1
  
  def __mul__(self,other):
    t=self.pages*other.pages
    return t
  def __sub__(self,other):
    t2=self.pages-other.pages
    return t2
  
b1=venky(100)
b2=venky(200)
b3=venky(300)
print(b1+b2)
print(b1*b2)
print(b1-b3)

