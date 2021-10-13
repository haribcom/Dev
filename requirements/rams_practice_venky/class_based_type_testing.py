class typetest:
    def test(self,instance,*args):
        if instance=='int':
            result=0
            for i in args:
                result+=i
        if instance=='str':
            result=''
            for i in args:
                j=str(i)
                result+=j
        print(result)
type1=typetest()
type1.test('int',10,20,30,40)
type1.test('str',10,20,30,40)
