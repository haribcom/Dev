import re

a=re.finditer(r"a{5}","aafhdkhjsaaaaahjgwaaaaa")
for i in a:
  print(i.group())
