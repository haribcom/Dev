def venky():
    n = 1
    print("this is first one")
    yield n
    n += 1
    print("this is a second one")
    yield n
    n += 1
    print("this is a third one")
    yield n

for i in venky():
    print(i)


"""while True:
    try:
        print(next(v))
        print(next(v))
        print(next(v))
        print(next(v))

    except:
        print("NO more")
        break
        
"""
