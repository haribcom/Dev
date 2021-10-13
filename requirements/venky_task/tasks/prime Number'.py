n=int(input("enter a range: "))
b=[]

for i in range(n):
  for j in range(2,i):
    if i%j==0:
      break
  else:
    b.append(i)
print("prime numbers",b)
