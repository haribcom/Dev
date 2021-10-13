a="1001012011402100412"

#"0000000412"

z=[]
s=""
for i in a:
  if int(i)==0:
    z.clear()
    s=s+i
  elif int(i)!=0:
    z.append(i)
for j in z:
  s=s+str(j)
print(s)
    
    

