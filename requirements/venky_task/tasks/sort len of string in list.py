a=['pytho',"venky","venn","venkat",'v','ve',"ven","venn","a"]
d=dict()
b=[]
for i in range(len(a)):
  d[a[i]]=str(len(a[i]))
print(d)
for i in sorted(d.values()):
  for j in d.items():
    if i==j[-1] and j[0] not in b:
      b.append(j[0])
print(b)
