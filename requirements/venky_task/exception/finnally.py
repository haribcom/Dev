x=1
try:
    x=open("venky.txt")
    print("the file is opened")
    print(x.read())
except:
    print("error occured")
finally:
    if x!=2:
        x.close()
        print("file is closed")
