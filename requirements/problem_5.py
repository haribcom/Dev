def Unique():
    a=input('enter values: ')
    b=[]
    for i in a.split(','):
        b.append(int(i))
    c=[[]]
    for i in range(-1,len(b)+1):
        for j in range(-1,i):
            if [b[j]] not in c:
                c.append([b[j]])
                if (j+1)<len(b):
                    if [b[j],b[j+1]] and [b[j+1],b[j]] not in c:
                        c.append([b[j],b[j+1]])
                        if (j+2)<len(b):
                            if [b[j],b[j+2]] and [b[j+2],b[j]] not in c:
                                c.append([b[j],b[j+2]])
                                if [b[j],b[j+1],b[j+2]] and [b[j+1],b[j],b[j+2]] and [b[j+2],b[j+1],b[j]] not in c:
                                    c.append([b[j],b[j+1],b[j+2]])
    print(c)
Unique()
