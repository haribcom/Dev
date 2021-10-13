import re
a=input("enter a mobile number:")
b=re.findall(r"[6789][0-9]{9}",a)
if b!=None:
  print("the matched....")
else:
  print("not matched....")
