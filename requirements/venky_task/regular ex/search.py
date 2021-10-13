import re
n=input("enter a string: ")
a=re.search(n,"venkyvenkat")
if a!=None:
  print("the match is available :")
  print("the biginig index is:{} end index is: {} ".format(a.start(),a.end()))
else:
  print("not available")
    
