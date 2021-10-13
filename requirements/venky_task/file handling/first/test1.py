fname=input("enter a file  name: ")
f=open("d:\\vv\\"+fname,"r")
#feedback=input("this is file concept: ")
#print(f.read())
#f.write(feedback)
print(f.readlines(50))

#for i in f:
 # print(i,end="")
f.close()
