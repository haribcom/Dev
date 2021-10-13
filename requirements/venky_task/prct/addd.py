def add(a,b,c):
    sum=a+b+c
    if a==b and b==c:
        sum=sum*2
        return sum
    return sum
print(add(4,4,4))
