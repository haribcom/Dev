pos = 0
def search(l, n):
    low = 0
    high = len(l)
    for i in range(high):
        mid = (low+high)//2
        if l[mid] == n:
            globals()['pos'] = mid
            return True
        elif n > l[mid]:
            low = mid
        else:
            high = mid
    

l = [1, 5, 6, 10, 127, 9]
l.sort()
print(l)

n = int(input("enter number :"))
if search(l, n):
    print("found at", pos)
else:
    print("not found")

