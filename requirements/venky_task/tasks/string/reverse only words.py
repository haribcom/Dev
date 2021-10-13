n=input("enter a string: ")

for i in n.split():
  print(i[::-1],end=" ")

m=n.split()
print(m)
a=[]
for i in range(len(m)):
  if i%2==0:
    a.append(m[i])
    
  else:
    p=m[i]
    a.append(p[::-1])
    
print(a)

  
