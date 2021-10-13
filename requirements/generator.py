##def my_gen():
##    n = 1
##    print('This is printed first')
##    yield n
##    n += 1
##    print('This is printed second')
##    yield 
##for i in my_gen():
##    print (i)

    
##def my_gen(n):
##    num = int(input('enter divisible no. : '))
##    for i in range(num, n+1, num):
##       yield i
##
##it = my_gen(n=(int(input("enter range :"))))
##while True:
##    try:
##        print(next(it))
##    except StopIteration:
##        break
    



def rev_str(my_str):
    for i in range(len(my_str)-1, -1, -1):
        yield my_str[i]

res = []
for i in rev_str(input('enter a number that you want to reverse : ')):
    res.append(int(i))
print(res)
