class v:
    def add(self,instance,*args):
        if instance=="int":
            result=0
            for i in args:
                result=result+i
        #print(result)
        if instance=="str":
            result=" "
            for i in args:
                j=str(i)
                result=result+j
        print(result)

        
v1=v()
v1.add("int",10,20,30)
v1.add("str",10,20,30)
