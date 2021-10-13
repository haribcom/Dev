class venky:
  def m1(self,a=None,b=None,c=None):
    if a!=None and b!=None and c!=None:
      print("the total :",a+b+c)
    elif a!=None and b!=None:
      print("sum of a and b is:",a+b)
    else:
      print("please privide 2 or 3 arguments")
t1=venky()
t1.m1(10,20,30)
t1.m1(10,20)
t1.m1(10)

print()

class venkat():
  def m2(self,*a):
    total=0
    for i in a:
      total=total+i
    print("The sum is :",total)
t2=venkat()
t2.m2(10,20,30,50)
t2.m2(10)
t2.m2()
