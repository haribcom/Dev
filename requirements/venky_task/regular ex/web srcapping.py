import re,urllib
import urllib.request

l=["http://google.com"]
for i in l:
  print("Searching....",i)
  u=urllib.request.urlopen(i)
  t=u.read()
  title=re.findall("<title>.*</title>",str(t))
  print(title)
