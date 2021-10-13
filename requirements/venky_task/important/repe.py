s="Aaaaioufff"
a=""
c=0
for i in s:
  if i not in a:
    a=a+i
    e=s.count(i)
    c+=e
print(a,'+',c)
