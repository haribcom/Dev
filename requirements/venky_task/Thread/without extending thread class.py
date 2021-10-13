from threading import *

class test():
  def ven(self):
    print("This is without extending thread class ")
obj=test()
t=Thread(target=obj.ven)
t.start()
