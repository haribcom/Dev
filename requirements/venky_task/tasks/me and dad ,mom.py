s="me and mom asked to uncle for dad"
a=[]
k=0
for i in s.split():
  k+=1
  if i== i[::-1]:
    a.append(i)
print(a)


