a='abcdefgh'
b="xyz"
c=1234678
d=str(c)
for i in range(len(a)):
    try:
        print(a[i]+b[i]+d[i])
    except:
        try:
            print(a[i]+d[i])
        except:
            print(a[i])
                
