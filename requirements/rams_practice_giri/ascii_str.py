a=input('enter the string')
result=[ chr(ord(i)-32) for i in a]
print(result)
result2=''
for j in a:
    k=chr(ord(j)-32)
    result2+=k
print(result2)
    
