n=int(input("enter a range: "))

b=[]
for i in range(n):
  name=input("enter a name and marks : ")
  b.append(name.split(" "))
print(b)

for j in b:

  for k in j:
  
    sname=input("enter sname: ")
    if k==sname:
      t=0
      for h in range(len(j)):
        if h!=0:
          t=t+int(j[h])
      print(sname)
      print(t/(len(j)-1))
    else:
      print("student Not Found Please enter currect name....")

  

             
