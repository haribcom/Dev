def venky(a):
    for i in a:
        out=''
        t=i
        while(t>0):
            out=out+"*"
            t=t-1
        print(out)


#c=input("enter a words:")
venky([1,2,3,1,5,8])
