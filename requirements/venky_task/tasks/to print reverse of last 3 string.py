s="venkatesh"
a=s[:-4]
for i in range(len(s)-len(a)):
  p=(len(s)-1)-i
  a=a+s[p]
print(a)
  
