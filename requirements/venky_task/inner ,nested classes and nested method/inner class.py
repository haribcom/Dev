class Outer():
  def __init__(self):
    print("This is a Outer  class object creation")
  def m1(self):
    print("This is outer class method")
  class Inner():
    def __init__(self):
      print("This is  Inner class object creation ")
    def m1(self):
      print("Hi... This is inner class method")

Outer().Inner().m1()

"""i=Outer().Inner()
i.m1()"""
Outer().m1()

"""o=Outer()
i=o.Inner()
i.m1()"""
