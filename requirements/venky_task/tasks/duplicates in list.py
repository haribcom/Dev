a = [1,1,2,3,3,4,5,5,6,7,7]
b=[]
d=[]
for i in a:
  if i not in b:
    b.append(i)
  else:
    d.append(i)
    
print(b)
print(d)
