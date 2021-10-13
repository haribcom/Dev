import re
n=input("enter a string: ")
a=re.fullmatch("venkyvenkat",n)
if a!=None:
  print("the match is available :")
  print("the biginig index is:{} end index is: {} ".format(a.start(),a.end()))
else:
  print("not available")
print(a)

