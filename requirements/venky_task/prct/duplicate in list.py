a=[10,20,30,20,10,20,40,50,20,60]
b=[]
c=[]
for i in a:
    if i not in b:
        b.append(i)
    else:
        c.append(i)
print(b)
print(c)
