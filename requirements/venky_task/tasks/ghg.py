import re
n=int(input("enter a number: "))
b=[]
for i in range(n):
  email=input("enter a mail :")
  m=re.fullmatch("[a-z]+[-_]*[0-9]+@[a-z]+.com",email)
  if m!=None:
    b.append(email)
print(b)
