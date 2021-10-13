n=input("enter a string: ")
m=n.split(" ")
print(m)

print(" ".join(m[::-1]))
print()

n=m[::-1]
for i in n:
  print(i,end=" ")
