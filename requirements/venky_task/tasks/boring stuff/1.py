# "venkatesh"
# "vhesnekta"

s="venkat"
s1=""
l=len(s)-1
if len(s1)<len(s):
  for i in range(len(s)):
    s1=s1+s[i]
    for j in range(l,l-1,-1):
      p=l-j
      s1=s1+s[p]
    l=l-1
print(s1)
    
    
  

  
  
