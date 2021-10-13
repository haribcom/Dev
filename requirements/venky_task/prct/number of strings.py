def venky(str,n):
    f=''
    for i in range(n):
        f=f+str
    return repr("%s %s"%(f,t))
s=str(input("enter aur name:"))
t=int(input("ente a n no'of times u want:"))
print(venky(s,t))

