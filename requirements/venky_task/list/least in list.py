a=[10,20,-1,40,506,2,-200,3]
b=[]
for i in a:
  if i not in b:
    b.append(i)
  b.sort()
  print(b)
  print(b[0])
