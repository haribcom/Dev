class venky():
    a=1000
    b=2000
    def m1(self):
        print(venky.a)
        print(venky.b)
        
    def m2(self):
        venky.a=venky.a+100
        venky.b=venky.b+100
v1=venky()
v1.m1()
v1.m2()
v1.m1()
v1.m2()
v1.m1()
v1.m2()

