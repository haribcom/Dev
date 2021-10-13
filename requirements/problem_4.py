def Difmax():
    n=int(input('enter range: '))
    a=[]
    for i in range(n):
        b=int(input('enter value: '))
        a.append(b)
    r=[]
    for i in range(len(a)):
        for j in range(i):
            r.append(abs(a[j]-a[j+1]))
    print(max(r))

Difmax()
    







    
        
