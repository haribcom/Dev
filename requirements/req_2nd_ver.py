
a='abcdefgh'
b="xyznnnnnn"
c=12346
d=str(c)
level = max(len(a), len(b), len(d))
for i in range(level):
    try:
        print(a[i]+b[i]+d[i])
    except:
        try:
            print(a[i]+d[i])
        except:
            print(a[i])










##a = 'abcdefgh'
##b = 'xyz'
##c = 1234
##d = str(c)
##e = (len(a),len(b),len(d))
##s = []
##for i in range(max(e)):
##    if i < len(a):
##        if i < len(b):
##            if i < len(d):
##                s.append(a[i]+b[i]+d[i])
##            else:
##                s.append(a[i]+b[i])
##        elif i < len(d):
##            s.append(a[i]+d[i])
##        else:
##            s.append(a[i])
##    elif i < len(b):
##        if i < len(d):
##            s.append(b[i]+d[i])
##        else:
##            s.append(b[i])
##    else:
##        s.append(d[i])
##print(s)
##
##res = ','.join(s)
##print (res)
##
##
