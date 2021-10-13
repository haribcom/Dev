start = int(input("enter starting range :"))
ending = int(input("enter given range :"))
arm = []
for i in range(start, ending+1):
    sum1 = 0
    temp = i
    order = len(str(i))
    while i > 0:
        digit = i % 10
        sum1 += digit**order
        i //= 10
    if temp == sum1:
        arm.append(temp)
print (arm)


''' ---Checking Armsrong or not--- '''

num = int(input("Enter a number :"))
sum1 = 0
temp = num
order = len(str(num))
while num > 0:
    digit = num%10
    sum1 = sum1+digit**order
    num //= 10

if temp == sum1:
    print (temp," is a armstrong number")
else :
    print (temp," is not a armstrong number")
