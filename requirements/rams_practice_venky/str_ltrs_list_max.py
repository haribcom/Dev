l=['rams','raghu','krish','siva','linga']
d=dict()
c=0
b=input('enter the letters::')
for i in l:
    f=c
    for j in b:
        if j in i:
            c+=1
            d[i]=c-f
print(d)
s=max(d.values())
for h in d.items():
    #(rams,2)
    #print(h[1])
    if s==h[1]:
        print(str(h[0]),'have max letters from',str(b),':',s)
        
