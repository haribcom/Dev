import re

d={}
with open("venky.txt","r")as f:
  for i in f:
    name=re.findall(r"[a-zA-Z]+",i)
    age=re.findall(r"[0-9]{1,3}",i)
    s=0
    
    for eachname in name:
      d[eachname]=age[s]
      s+=1
  print(d)
    
