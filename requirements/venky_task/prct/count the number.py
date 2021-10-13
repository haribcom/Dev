def venky(s):
    b=[]
    a=[]
    c=[]
    for i in s:
        b.append(i)
    for j in b:
        if j not in a:
            a.append(j)
        
        else:
            c.append(j)
    for k in a:
        print(k,end="")
s=str(input("enter your number :"))
venky(s)
