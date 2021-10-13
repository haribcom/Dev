import re
n=input("enter a string: ")
a=re.match(n,"venkyvenkat")
if a!=None:
  print("the match is available :")
  print("the biginig index is:{} end index is: {} ".format(a.start(),a.end()))
  print("group is ",a.group())
else:
  print("not available")
    
