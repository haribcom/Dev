import re
count=0
a=input("enter a : ")
match=re.findall(a,"aaevfvhdva")
if match!=None:
  print("is available")
  print(match.start(),"....",match.group())
else:
  print("not avalible")

'''a=re.subn("\d","*","venky@1236")
print(a)
print(a[0])
print(a[1])'''
