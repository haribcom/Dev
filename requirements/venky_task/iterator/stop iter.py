a=[10,20,30,40,50]
it=iter(a)
while True:
    try:
        print(next(it))
    except:
        print("error occured")
        break
