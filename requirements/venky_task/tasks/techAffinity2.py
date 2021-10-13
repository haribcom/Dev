import re
b=[]
a=re.finditer(r"1+","10001111011101111000")
for i in a:
  b.append(i.group())
b.sort()
print(len(b[-1]))
