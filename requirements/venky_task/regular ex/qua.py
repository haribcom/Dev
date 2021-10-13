import re
count=0
p=re.finditer(r"a","bb  bbbaaabbabdf")#"a*,a+,a?,a"
for i in p:
  count+=1
  print(i.group())
print(count)
