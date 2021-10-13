a=input("enter a Fno:")
b=input("enter a Sno:")
try:
    i=int(a)
    j=int(b)
    c=i/j
    print(c)

except(ValueError):
    print("plz enter numeric values")
except(ZeroDivisionError):
    print("sno can't zero")
except():
    print("error occured")
finally:
    print("i got it")
