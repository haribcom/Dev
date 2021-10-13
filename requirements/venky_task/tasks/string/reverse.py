n=input("enter a string: ")
print(n[::-1])
print()

t=1
for i in range(len(n)):
  s=len(n)-t
  print(n[s],end="")
  t=t+1
print()
print()

a=''
i=len(n)-1
while i>=0:
  a=a+str(n[i])
  i=i-1
print(a)
print()

d=reversed(n)
print("".join(d))
  
