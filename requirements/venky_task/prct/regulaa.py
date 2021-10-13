import re
matcher=re.finditer("\S","ajhddfj#47  63498fh")

for i in matcher:
  print(i.start(),i.end(),i.group())
