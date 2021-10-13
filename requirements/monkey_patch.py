import m
def new_f(self):
    return "monkey_f()"
m.MyClass.f=new_f
obj=m.MyClass()
obj.f()
