import re
pattern=re.compile("1+")
match=pattern.finditer("ven111kyv11enk11at")
for i in match:
  print("the available of the indexs: ",i.start())
  print(" the end index of the indexs :",i.end())
  print(i.end()-i.start())
  print(i.group())
