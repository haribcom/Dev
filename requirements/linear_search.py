pos = -1

def search(l, num):
    for i in range(len(l)):
        if l[i] == num:
           globals()['pos'] = i+1
           return True



l = [1, 2, 3, 4, 4, 5, 6, 7, 9]
num = int(input("enter number you search :"))
search(l, num)
if num in l:
    print("found at {}".format(pos))
else:
    print("not found")

