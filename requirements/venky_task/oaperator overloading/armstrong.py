n=int(input("enter the number"))
s=str(n)
a=0
for i in range(len(s)):
  a=a+(int(s[i])**3)
if a==n:
  print(n,"it's armstorng number")
else:
  print("Not a armstrong")
  
  
  
