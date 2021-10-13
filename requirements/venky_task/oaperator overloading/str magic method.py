class venky():

  def __init__(self,pages):
    self.pages=pages

  def __str__(self):
    return "the no'f pages is :"+str(self.pages)

  def __add__(self,other):
    t=self.pages+other.pages
    a=venky(t)
    return a


b1=venky(100)
b2=venky(200)
b3=venky(300)

print(b1+b2+b3+b2)

"""whenever we are calling + operator ther __add__() method will be called."""
"""whenenve we are printing venky object references ther __str__() will be  called"""
