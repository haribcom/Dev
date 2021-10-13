a=["venky","venkat","raju","karthik","anilll","saran"]

b=input("enter a string: ")
d=dict()
c=0
for i in a:
  f=c
  for j in b:
    if j in i:
      c+=1
      d[i]=c-f
print(d)
s=max(d.values())
for h in d.items():
  if s==h[1]:
    print(str(h[0]),"have max letters from",str(b),":",s)
      
      
