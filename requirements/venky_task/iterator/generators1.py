def rev_str(my_str):
    length=len(my_str)
    for i in range(length-1,-1,-1):
        yield my_str[i]

it=rev_str("venky")
#print(next(it))
#print(next(it))
for i in it:
    print(i)
