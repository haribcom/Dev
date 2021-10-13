f=open("venky.txt","r")
a=[]
for  i in f:
  b=i.split()

  for j in b:
    a.append(j)
print(a)
print(len(a))
for k in a:
  pass  
f.close()
  
