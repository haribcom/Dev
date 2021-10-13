import re
i=0
a=re.finditer("\s","fhdgsf jhjf")
for j in a:
  i=i+1
  print(j.group())
print(i)
  #\s,\w,\W,\d,\D
