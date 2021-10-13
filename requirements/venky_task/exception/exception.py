class ValueTooSmall(Exception):
    pass
class ValueTooLarge(Exception):
    pass
n=100
while True:
    try:
        a=int(input("enter a your searching number"))
        if a<n:
            raise ValueTooSmall
        elif a>n:
            raise ValueTooLarge
        break
    except(ValueTooSmall):
        print("your given number is small")
    except(ValueTooLarge):
        print("the given number is large")
print("yess u got it")

    
