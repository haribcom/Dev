import re,urllib
import urllib.request
u=urllib.request.urlopen("https://www.findandtrace.com/mobile-phone-number-database/Andhra-Pradesh/IDEA")
print(type(u))
r=u.read()
r=re.findall(r"[9]{1}[0-9]{9}",str(r))
for i in r:
  print(i)
