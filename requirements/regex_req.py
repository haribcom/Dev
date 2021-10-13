import re

s = '120340500650550999'

ss = re.search('0.*0', s).group()
print(ss)
sss = re.sub('[1-9]', '', ss)
print(sss)
res = s.split('0')
print(res)
out = sss+str(res.pop())
print(out)
