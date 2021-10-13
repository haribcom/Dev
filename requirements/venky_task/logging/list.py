
n=input("enter a num:")
a=[]
c=0
for i in n.split(","):
  a.append(int(i))
a.sort()
print(a)
