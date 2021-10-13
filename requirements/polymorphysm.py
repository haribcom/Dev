class X:
    def add(self,instanceOf,*args):
        if instanceOf=='init':
            self.result=0
        if instanceOf=='str':
            self.result=' '
        for i in args:
            self.result+=i
        print(self.result)
x1=X()
x1.add('init',10,20,30)
x1.add('str','giri','honey')
