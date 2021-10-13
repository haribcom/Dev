a=[34,67,786,3533,6,45]
b=["venk","ven","venkyyy","vennn"]
for i in range(len(a)):
  for j in range(len(a)):
    if a[(i)]>a[(j)]:
      t=a[i]
      a[i]=a[j]
      a[j]=t
print(a)
n=int(input("enter a  number: "))
n2=int(input("enter second number: "))
for i in range(len(a)):
  if a[i]==n or a[i]==n2:
    if a[i]==n:
      print("The first element",a[i],"position is ",i)
    elif a[i]==n2:
      print("the second element",i,"th Index is ",a[i])
  else:
    print("element NOt found....")
    break
    
