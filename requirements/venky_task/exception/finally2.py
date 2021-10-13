x=None
try:
    x=open("venkat.txt")
    print("file is opened")
    print(x.read())
    x.write("apssdc")
except:
    print("error occured")
finally:
    if x!=None:
        x.close()
        print("file is clodsed")
