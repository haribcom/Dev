def shuf(List):
    import random
    newList=[]
    for i in List:
        i=random.choice(List)
        newList+=i
    return newList
x = shuf("Honey")
print(x)
