n=input("enter a number: ")
s=""
l=len(n)-1
for i in range(len(n)):
  p=l-i
  s=s+n[p]
if s==n:
  print("It's a palindrome")
else:
  print("it's Not  a palindrome")
