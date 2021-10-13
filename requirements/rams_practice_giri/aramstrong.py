s=int(input('enter the starting point'))
e=int(input('enter the ending point'))
result=[]
for i in range(s,e+1):
    order=len(str(i))
    #print(length)
    samu=0
    t=i
    while i>0:
        digit=i%10
        tot=digit**order
        samu+=tot
        i//=10
    if t==samu:
        result.append(t)
        
print(result)
#checking armstrong or not
num=int(input('enter the number'))
temp=num
sum1=0
order=len(str(num))
while num>0:
    digit=num%10
    sum1+=digit**order
    num//=10
if temp==sum1:
    print(temp,'this is armstrong')
else:
    print(temp,'this is not armstrong')
