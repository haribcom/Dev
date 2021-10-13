s=input("enter a string: ")
t=1
for i in range(len(s)):
  p=len(s)-t
  
  print(s[p],end="")
  t=t+1



print()
n=input("enter a string: ")
a=""
l=len(n)-1
while l>=0:
  a=a+n[l]
  l=l-1
print(a)



