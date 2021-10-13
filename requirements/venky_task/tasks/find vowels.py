n=input("enter string: ")
v="aeiou"
a=[]
for i in range(len(n)):
  
  if n[i] in v:
    j=0
    for k in n[i+1:]:
      if k in v:
        break
      j=j+1
      a.append(j)
if a[-1]>=2:
  print(a[-1])
else:
  print("-1")

      
  
  
