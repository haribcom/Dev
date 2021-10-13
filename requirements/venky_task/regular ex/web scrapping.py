import re
import urllib
import urllib.request


l=["http://google.com","http://www.softapt.in/"]

for i in l:
  print("Searching....")
  u=urllib.request.urlopen(i)
  t=u.read()
  s=re.findall("<title>.*</title>",str(t),re.IGNORECASE)
  print(s)
