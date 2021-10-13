# Reverse a Number
n=int(input("Eenter number :"))
rev=0
while n>0:
    dig=n%10
    rev=rev*10+dig
    n//=10
print rev





inp = input("enter number or string :")
try:
    if int(inp):
        rev = int(inp[::-1])
        print(rev)
except:
    print(inp[::-1])
