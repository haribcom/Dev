import re
s=["bed","bath","bedbath","and","beyond"]
s2=[]
ss="bedbathandbeyond"
n=0
while n<len(ss):
  for i in s:
    m=re.match(i,ss[n:])
    if m!=None:
      s2.append(m.group())
      n=n+len(i)
print(s2)
      
    
